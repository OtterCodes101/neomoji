# Mastodon API Konfiguration
MASTODON_ACCESS_TOKEN = "DEIN_ACCESS_TOKEN"
MASTODON_INSTANCE = "https://deine.instance.social"
DEFAULT_LIMIT = 40  # Standardwert für die Anzahl der Erwähnungen

def setup_headers():
    # ... existing code ...

def get_mentions(headers, limit=DEFAULT_LIMIT):
    # Hole Erwähnungen mit angegebener Limit
    url = f"{MASTODON_INSTANCE}/api/v1/notifications"
    params = {
        'types[]': 'mention',
        'limit': min(limit, 400)  # Maximales Limit von 400
    }
    
    mentions = []
    while len(mentions) < limit:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            break
            
        batch = response.json()
        if not batch:
            break
            
        mentions.extend(batch)
        
        # Hole die nächste Seite, falls verfügbar und noch nicht genug Erwähnungen
        links = response.links if hasattr(response, 'links') else {}
        if 'next' in links and len(mentions) < limit:
            url = links['next']['url']
        else:
            break
    
    return mentions[:limit]

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Prüfe unbeantworte Mastodon-Erwähnungen')
    parser.add_argument('--limit', type=int, default=DEFAULT_LIMIT,
                      help='Anzahl der zu prüfenden Erwähnungen (40-400)')
    
    args = parser.parse_args()
    
    # Stelle sicher, dass das Limit im erlaubten Bereich liegt
    limit = max(40, min(400, args.limit))
    
    headers = setup_headers()
    mentions = get_mentions(headers, limit=limit)
    
    unanswered_mentions = []
    
    for mention in mentions:
        if not has_user_responded(headers, mention):
            unanswered_mentions.append(mention)
    
    create_html_report(unanswered_mentions)
    print(f"Bericht wurde erstellt: {len(unanswered_mentions)} unbeantworte Erwähnungen von {len(mentions)} geprüften Erwähnungen") 