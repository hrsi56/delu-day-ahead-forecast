"""Read-only documentation refresh; saves cached bytes outside tracked report paths.

Never downloads commodity/forecast/outage observations or any pre-2019 model input.
"""
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
from urllib.request import Request, urlopen

SOURCES = {
    'entsoe_mop_v3r5': 'https://eepublicdownloads.blob.core.windows.net/public-cdn-container/clean-documents/mc-documents/transparency-platform/MOP/MoP_v3r5_final.zip',
    'entsoe_reuse': 'https://transparencyplatform.zendesk.com/hc/article_attachments/40921869379729',
    'smard_reuse': 'https://www.smard.de/home/datennutzung',
    'eex_gas': 'https://www.eex.com/en/markets/natural-gas/gas-market-transparency',
    'eex_the': 'https://webshop.eex-group.com/data-type/eex-natural-gas-file-cloud-eod',
    'eex_eua_catalogue': 'https://www.eex.com/de/downloads',
    'eex_terms_v8': 'https://www.eex.com/fileadmin/EEX/Downloads/Market_Data/EEX_Group_DataSource/General_Terms_of_Contract/WIP_Datasource_GC-v8_FINAL.pdf',
    'eex_de_outages': 'https://www.eex-transparency.com/power/de/umms',
    'jao_da_handbook': 'https://publicationtool.jao.eu/core/CORE_PublicationHandbook',
    'jao_id_handbook': 'https://www.jao.eu/sites/default/files/2025-10/Core_IDCC_PublicationTool_Handbook_v1.6.pdf',
    'jao_core_start': 'https://www.jao.eu/news/core-announcement-go-live-readiness',
    'worldbank_commodities': 'https://www.worldbank.org/en/research/commodity-markets',
    'mastr': 'https://www.bundesnetzagentur.de/DE/Fachthemen/ElektrizitaetundGas/Monitoringberichte/Marktstammdatenregister/start.html',
    'weather_forecast_archive': 'https://open-meteo.com/en/docs/historical-forecast-api',
    'weather_previous_runs': 'https://open-meteo.com/en/docs/previous-runs-api',
    'weather_terms': 'https://open-meteo.com/en/terms',
}
if __name__ == '__main__':
    cache = Path('data/cp15-probe-cache/sources')
    cache.mkdir(parents=True, exist_ok=True)
    rows = []
    for name, url in SOURCES.items():
        row = {'id':name, 'url':url, 'retrieved_at_utc':datetime.now(timezone.utc).isoformat()}
        try:
            with urlopen(Request(url, headers={'User-Agent':'CP15-readonly-feasibility/1.0'}), timeout=30) as response:
                data = response.read(30 * 1024**2)
                row.update(status=response.status, resolved_url=response.url, content_type=response.headers.get('Content-Type'))
            path = cache/(name+'.source')
            path.write_bytes(data)
            row.update(bytes=len(data), sha256=sha256(data).hexdigest(), cache_path=str(path))
        except Exception as exc:
            row.update(status='retrieval_failed', error_type=type(exc).__name__)
        rows.append(row)
        print(name, row['status'])
    Path('reports/cp15/feasibility/source_retrieval_manifest.json').write_text(json.dumps(rows,indent=2)+'\n')
