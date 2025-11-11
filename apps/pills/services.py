import logging
import requests
from django.conf import settings

log = logging.getLogger(__name__)

def fetch_pills_from_public_api(*, entp_name=None, item_name=None, efcy_qesitm=None, page=1, page_size=20):

    if not settings.MFDS_API_KEY:
        raise RuntimeError("MFDS_API_KEY not configured")

    params = {
        "serviceKey": settings.MFDS_API_KEY,
        "type": "json",
        "pageNo": page,
        "numOfRows": page_size,
    }
    if item_name:
        params["itemName"] = item_name
    if entp_name:
        params["entpName"] = entp_name
    if efcy_qesitm:
        params["efcyQesitm"] = efcy_qesitm

    print(params)
    try:
        resp = requests.get(settings.MFDS_BASE_URL, params=params, timeout=8)
        resp.raise_for_status()
        data = resp.json()

        body = None
        if isinstance(data, dict):
            body = data.get("body") or data.get("response", {}).get("body") or data
        total = int(body.get("totalCount", 0)) if isinstance(body, dict) else 0
        items = (body.get("items") or []) if isinstance(body, dict) else []

        normalized = []
        for it in items:
            normalized.append({
                "item_seq": str(it.get("itemSeq") or it.get("ITEM_SEQ") or ""),
                "item_name": it.get("itemName") or it.get("ITEM_NAME") or "",
                "entp_name": it.get("entpName") or it.get("ENTP_NAME") or "",
                "efcy_qesitm": it.get("efcyQesitm") or it.get("EFCY_QESITM") or "",
                "use_method_qesitm": it.get("useMethodQesitm") or it.get("USE_METHOD_QESITM") or "",
                "atpn_warn_qesitm": it.get("atpnWarnQesitm") or it.get("ATPN_WARN_QESITM") or "",
                "intrc_qesitm": it.get("intrcQesitm") or it.get("INTRC_QESITM") or "",
                "se_qesitm": it.get("seQesitm") or it.get("SE_QESITM") or "",
                "deposit_method_qesitm": it.get("depositMethodQesitm") or it.get("DEPOSIT_METHOD_QESITM") or "",
                "item_image_url": it.get("itemImage") or it.get("ITEM_IMAGE") or "",
            })
        return total, normalized
    except Exception as e:
        log.exception("Public API error")
        raise
