ITEM_SEQ_MAP = {
  '29002': 'Opiqutan_Soft_Cap',
  '34342': '201804518',
  '37990': '201804518',
  '39916': 'Uniteride_Tab',
  '40122': 'Unikamin_Tab',
  '40720': 'New_Glia_Tab',
  '40767': 'Gestaren_2X_Tab',
  '40792': 'Diacell_Cap',
  '40837': 'Duosta_Tab',
  '40949': 'Afental_CR_Tab',
  '40953': 'Canagabarotin_Cab',
  '40990': 'Sebaco_Hct_Tab',
  '40991': 'Sebaco_Hct_Tab',
  '41097': '202106054',
  '41107': 'Anacox_Cap',
  '41169': 'Razarect_Tab',
  '41170': 'Leviepil_Tab',
  '41172': 'Leviepil_Tab',
  '41207': 'Vtamin_Tab',
  '41225': 'T-muse_soft_Cap',
  '41327': 'Rabeprazole_Tab',
  '41344': 'Tovast_Tab',
}
#DB저장값을 아이템 시퀸스로 치환
def map_to_item_seq(db_value: str) -> str:
    return ITEM_SEQ_MAP.get(db_value, "")