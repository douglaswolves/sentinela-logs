"""Análise local de eventos de autenticação em JSON Lines (Python 3.10+)."""
import argparse
from collections import defaultdict, deque
from datetime import datetime, timedelta, timezone
import ipaddress
import json
from pathlib import Path


def load_events(path):
    events, rejected = [], []
    with Path(path).open(encoding='utf-8') as source:
        for number, line in enumerate(source, 1):
            if not line.strip():
                continue
            try:
                event = json.loads(line)
                if not isinstance(event, dict):
                    raise ValueError('evento deve ser um objeto')
                timestamp = datetime.fromisoformat(event['timestamp'].replace('Z', '+00:00'))
                if timestamp.utcoffset() is None:
                    raise ValueError('timestamp precisa conter fuso horário')
                if event['status'] not in ('failure', 'success'):
                    raise ValueError('status deve ser failure ou success')
                if not isinstance(event['user'], str) or not event['user'].strip():
                    raise ValueError('user deve ser texto não vazio')
                event['ip'] = str(ipaddress.ip_address(event['ip']))
                event['time'] = timestamp.astimezone(timezone.utc)
                events.append(event)
            except (ValueError, TypeError, KeyError, AttributeError) as error:
                rejected.append({'line': number, 'reason': str(error)})
    return sorted(events, key=lambda event: event['time']), rejected


def analyze(events, threshold=5, window=300):
    if threshold < 2 or window < 1:
        raise ValueError('threshold >= 2 e window >= 1 são obrigatórios')
    histories = defaultdict(deque)
    active = set()
    alerts = []
    for event in sorted(events, key=lambda item: item['time']):
        ip = event['ip']
        history = histories[ip]
        cutoff = event['time'] - timedelta(seconds=window)
        while history and history[0]['time'] < cutoff:
            history.popleft()
        if len(history) < threshold:
            active.discard(ip)
        if event['status'] == 'failure':
            history.append(event)
            if len(history) >= threshold and ip not in active:
                alerts.append({'rule': 'repeated_failures', 'severity': 'medium',
                               'ip': ip, 'timestamp': event['time'].isoformat(),
                               'failures': len(history),
                               'users': sorted({item['user'] for item in history})})
                active.add(ip)
        elif sum(item['user'] == event['user'] for item in history) >= threshold:
            alerts.append({'rule': 'success_after_failures', 'severity': 'high',
                           'ip': ip, 'user': event['user'],
                           'timestamp': event['time'].isoformat(),
                           'failures': sum(item['user'] == event['user'] for item in history)})
            # Uma autenticação bem-sucedida encerra a sequência desta conta.
            histories[ip] = deque(item for item in history if item['user'] != event['user'])
            if len(histories[ip]) < threshold:
                active.discard(ip)
    return alerts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path, help='arquivo JSONL')
    parser.add_argument('--threshold', type=int, default=5)
    parser.add_argument('--window', type=int, default=300, help='janela em segundos')
    parser.add_argument('--output', type=Path, help='salvar relatório JSON')
    args = parser.parse_args()
    if args.threshold < 2 or args.window < 1:
        parser.error('use threshold >= 2 e window >= 1')
    try:
        events, rejected = load_events(args.input)
        report = {'events': len(events), 'rejected_lines': rejected,
                  'settings': {'threshold': args.threshold, 'window_seconds': args.window},
                  'alerts': analyze(events, args.threshold, args.window)}
        result = json.dumps(report, ensure_ascii=False, indent=2)
        if args.output:
            args.output.write_text(result + '\n', encoding='utf-8')
        print(result)
    except (OSError, UnicodeError) as error:
        parser.exit(2, f'Erro ao acessar arquivo: {error}\n')


if __name__ == '__main__':
    main()
