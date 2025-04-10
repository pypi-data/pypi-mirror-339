# coding: UTF-8
import sys
bstack11l1ll1_opy_ = sys.version_info [0] == 2
bstack1111l11_opy_ = 2048
bstack1l11111_opy_ = 7
def bstack1ll1l1_opy_ (bstack1l1ll1_opy_):
    global bstack1l111ll_opy_
    bstack1lll1ll_opy_ = ord (bstack1l1ll1_opy_ [-1])
    bstack111llll_opy_ = bstack1l1ll1_opy_ [:-1]
    bstack1l1l11l_opy_ = bstack1lll1ll_opy_ % len (bstack111llll_opy_)
    bstack1l1l1l_opy_ = bstack111llll_opy_ [:bstack1l1l11l_opy_] + bstack111llll_opy_ [bstack1l1l11l_opy_:]
    if bstack11l1ll1_opy_:
        bstack11ll111_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l11_opy_ - (bstackl_opy_ + bstack1lll1ll_opy_) % bstack1l11111_opy_) for bstackl_opy_, char in enumerate (bstack1l1l1l_opy_)])
    else:
        bstack11ll111_opy_ = str () .join ([chr (ord (char) - bstack1111l11_opy_ - (bstackl_opy_ + bstack1lll1ll_opy_) % bstack1l11111_opy_) for bstackl_opy_, char in enumerate (bstack1l1l1l_opy_)])
    return eval (bstack11ll111_opy_)
import os
import re
from enum import Enum
bstack11ll1l1l1l_opy_ = {
  bstack1ll1l1_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬᙨ"): bstack1ll1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡹࡸ࡫ࡲࠨᙩ"),
  bstack1ll1l1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨᙪ"): bstack1ll1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡱࡥࡺࠩᙫ"),
  bstack1ll1l1_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪᙬ"): bstack1ll1l1_opy_ (u"ࠨࡱࡶࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ᙭"),
  bstack1ll1l1_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩ᙮"): bstack1ll1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡸࡷࡪࡥࡷ࠴ࡥࠪᙯ"),
  bstack1ll1l1_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩᙰ"): bstack1ll1l1_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹ࠭ᙱ"),
  bstack1ll1l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩᙲ"): bstack1ll1l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩ࠭ᙳ"),
  bstack1ll1l1_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ᙴ"): bstack1ll1l1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᙵ"),
  bstack1ll1l1_opy_ (u"ࠪࡨࡪࡨࡵࡨࠩᙶ"): bstack1ll1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡨࡪࡨࡵࡨࠩᙷ"),
  bstack1ll1l1_opy_ (u"ࠬࡩ࡯࡯ࡵࡲࡰࡪࡒ࡯ࡨࡵࠪᙸ"): bstack1ll1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡯ࡵࡲࡰࡪ࠭ᙹ"),
  bstack1ll1l1_opy_ (u"ࠧ࡯ࡧࡷࡻࡴࡸ࡫ࡍࡱࡪࡷࠬᙺ"): bstack1ll1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡯ࡧࡷࡻࡴࡸ࡫ࡍࡱࡪࡷࠬᙻ"),
  bstack1ll1l1_opy_ (u"ࠩࡤࡴࡵ࡯ࡵ࡮ࡎࡲ࡫ࡸ࠭ᙼ"): bstack1ll1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡴࡵ࡯ࡵ࡮ࡎࡲ࡫ࡸ࠭ᙽ"),
  bstack1ll1l1_opy_ (u"ࠫࡻ࡯ࡤࡦࡱࠪᙾ"): bstack1ll1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡻ࡯ࡤࡦࡱࠪᙿ"),
  bstack1ll1l1_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡍࡱࡪࡷࠬ "): bstack1ll1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡍࡱࡪࡷࠬᚁ"),
  bstack1ll1l1_opy_ (u"ࠨࡶࡨࡰࡪࡳࡥࡵࡴࡼࡐࡴ࡭ࡳࠨᚂ"): bstack1ll1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡶࡨࡰࡪࡳࡥࡵࡴࡼࡐࡴ࡭ࡳࠨᚃ"),
  bstack1ll1l1_opy_ (u"ࠪ࡫ࡪࡵࡌࡰࡥࡤࡸ࡮ࡵ࡮ࠨᚄ"): bstack1ll1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱࡫ࡪࡵࡌࡰࡥࡤࡸ࡮ࡵ࡮ࠨᚅ"),
  bstack1ll1l1_opy_ (u"ࠬࡺࡩ࡮ࡧࡽࡳࡳ࡫ࠧᚆ"): bstack1ll1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡺࡩ࡮ࡧࡽࡳࡳ࡫ࠧᚇ"),
  bstack1ll1l1_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩᚈ"): bstack1ll1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡡࡹࡩࡷࡹࡩࡰࡰࠪᚉ"),
  bstack1ll1l1_opy_ (u"ࠩࡰࡥࡸࡱࡃࡰ࡯ࡰࡥࡳࡪࡳࠨᚊ"): bstack1ll1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡰࡥࡸࡱࡃࡰ࡯ࡰࡥࡳࡪࡳࠨᚋ"),
  bstack1ll1l1_opy_ (u"ࠫ࡮ࡪ࡬ࡦࡖ࡬ࡱࡪࡵࡵࡵࠩᚌ"): bstack1ll1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲࡮ࡪ࡬ࡦࡖ࡬ࡱࡪࡵࡵࡵࠩᚍ"),
  bstack1ll1l1_opy_ (u"࠭࡭ࡢࡵ࡮ࡆࡦࡹࡩࡤࡃࡸࡸ࡭࠭ᚎ"): bstack1ll1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡭ࡢࡵ࡮ࡆࡦࡹࡩࡤࡃࡸࡸ࡭࠭ᚏ"),
  bstack1ll1l1_opy_ (u"ࠨࡵࡨࡲࡩࡑࡥࡺࡵࠪᚐ"): bstack1ll1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡵࡨࡲࡩࡑࡥࡺࡵࠪᚑ"),
  bstack1ll1l1_opy_ (u"ࠪࡥࡺࡺ࡯ࡘࡣ࡬ࡸࠬᚒ"): bstack1ll1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡺࡺ࡯ࡘࡣ࡬ࡸࠬᚓ"),
  bstack1ll1l1_opy_ (u"ࠬ࡮࡯ࡴࡶࡶࠫᚔ"): bstack1ll1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡮࡯ࡴࡶࡶࠫᚕ"),
  bstack1ll1l1_opy_ (u"ࠧࡣࡨࡦࡥࡨ࡮ࡥࠨᚖ"): bstack1ll1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡨࡦࡥࡨ࡮ࡥࠨᚗ"),
  bstack1ll1l1_opy_ (u"ࠩࡺࡷࡑࡵࡣࡢ࡮ࡖࡹࡵࡶ࡯ࡳࡶࠪᚘ"): bstack1ll1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡺࡷࡑࡵࡣࡢ࡮ࡖࡹࡵࡶ࡯ࡳࡶࠪᚙ"),
  bstack1ll1l1_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡈࡵࡲࡴࡔࡨࡷࡹࡸࡩࡤࡶ࡬ࡳࡳࡹࠧᚚ"): bstack1ll1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡩ࡯ࡳࡢࡤ࡯ࡩࡈࡵࡲࡴࡔࡨࡷࡹࡸࡩࡤࡶ࡬ࡳࡳࡹࠧ᚛"),
  bstack1ll1l1_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪ᚜"): bstack1ll1l1_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧ᚝"),
  bstack1ll1l1_opy_ (u"ࠨࡴࡨࡥࡱࡓ࡯ࡣ࡫࡯ࡩࠬ᚞"): bstack1ll1l1_opy_ (u"ࠩࡵࡩࡦࡲ࡟࡮ࡱࡥ࡭ࡱ࡫ࠧ᚟"),
  bstack1ll1l1_opy_ (u"ࠪࡥࡵࡶࡩࡶ࡯࡙ࡩࡷࡹࡩࡰࡰࠪᚠ"): bstack1ll1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡵࡶࡩࡶ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠫᚡ"),
  bstack1ll1l1_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡓ࡫ࡴࡸࡱࡵ࡯ࠬᚢ"): bstack1ll1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩࡵࡴࡶࡲࡱࡓ࡫ࡴࡸࡱࡵ࡯ࠬᚣ"),
  bstack1ll1l1_opy_ (u"ࠧ࡯ࡧࡷࡻࡴࡸ࡫ࡑࡴࡲࡪ࡮ࡲࡥࠨᚤ"): bstack1ll1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡯ࡧࡷࡻࡴࡸ࡫ࡑࡴࡲࡪ࡮ࡲࡥࠨᚥ"),
  bstack1ll1l1_opy_ (u"ࠩࡤࡧࡨ࡫ࡰࡵࡋࡱࡷࡪࡩࡵࡳࡧࡆࡩࡷࡺࡳࠨᚦ"): bstack1ll1l1_opy_ (u"ࠪࡥࡨࡩࡥࡱࡶࡖࡷࡱࡉࡥࡳࡶࡶࠫᚧ"),
  bstack1ll1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭ᚨ"): bstack1ll1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭ᚩ"),
  bstack1ll1l1_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭ᚪ"): bstack1ll1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡳࡰࡷࡵࡧࡪ࠭ᚫ"),
  bstack1ll1l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪᚬ"): bstack1ll1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪᚭ"),
  bstack1ll1l1_opy_ (u"ࠪ࡬ࡴࡹࡴࡏࡣࡰࡩࠬᚮ"): bstack1ll1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱࡬ࡴࡹࡴࡏࡣࡰࡩࠬᚯ"),
  bstack1ll1l1_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡘ࡯࡭ࠨᚰ"): bstack1ll1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡫࡮ࡢࡤ࡯ࡩࡘ࡯࡭ࠨᚱ"),
  bstack1ll1l1_opy_ (u"ࠧࡴ࡫ࡰࡓࡵࡺࡩࡰࡰࡶࠫᚲ"): bstack1ll1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡴ࡫ࡰࡓࡵࡺࡩࡰࡰࡶࠫᚳ"),
  bstack1ll1l1_opy_ (u"ࠩࡸࡴࡱࡵࡡࡥࡏࡨࡨ࡮ࡧࠧᚴ"): bstack1ll1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡸࡴࡱࡵࡡࡥࡏࡨࡨ࡮ࡧࠧᚵ"),
  bstack1ll1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡪࡸࡦࡇࡻࡩ࡭ࡦࡘࡹ࡮ࡪࠧᚶ"): bstack1ll1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡹ࡫ࡳࡵࡪࡸࡦࡇࡻࡩ࡭ࡦࡘࡹ࡮ࡪࠧᚷ"),
  bstack1ll1l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡕࡸ࡯ࡥࡷࡦࡸࡒࡧࡰࠨᚸ"): bstack1ll1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡶ࡫࡯ࡨࡕࡸ࡯ࡥࡷࡦࡸࡒࡧࡰࠨᚹ")
}
bstack11ll1l1l1l1_opy_ = [
  bstack1ll1l1_opy_ (u"ࠨࡱࡶࠫᚺ"),
  bstack1ll1l1_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬᚻ"),
  bstack1ll1l1_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬᚼ"),
  bstack1ll1l1_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩᚽ"),
  bstack1ll1l1_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠩᚾ"),
  bstack1ll1l1_opy_ (u"࠭ࡲࡦࡣ࡯ࡑࡴࡨࡩ࡭ࡧࠪᚿ"),
  bstack1ll1l1_opy_ (u"ࠧࡢࡲࡳ࡭ࡺࡳࡖࡦࡴࡶ࡭ࡴࡴࠧᛀ"),
]
bstack1ll1l1lll1_opy_ = {
  bstack1ll1l1_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪᛁ"): [bstack1ll1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡗࡖࡉࡗࡔࡁࡎࡇࠪᛂ"), bstack1ll1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡘࡗࡊࡘ࡟ࡏࡃࡐࡉࠬᛃ")],
  bstack1ll1l1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧᛄ"): bstack1ll1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆࡉࡃࡆࡕࡖࡣࡐࡋ࡙ࠨᛅ"),
  bstack1ll1l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩᛆ"): bstack1ll1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡖࡋࡏࡈࡤࡔࡁࡎࡇࠪᛇ"),
  bstack1ll1l1_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭ᛈ"): bstack1ll1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡕࡓࡏࡋࡃࡕࡡࡑࡅࡒࡋࠧᛉ"),
  bstack1ll1l1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬᛊ"): bstack1ll1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭ᛋ"),
  bstack1ll1l1_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬᛌ"): bstack1ll1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡁࡓࡃࡏࡐࡊࡒࡓࡠࡒࡈࡖࡤࡖࡌࡂࡖࡉࡓࡗࡓࠧᛍ"),
  bstack1ll1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫᛎ"): bstack1ll1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡆࡅࡑ࠭ᛏ"),
  bstack1ll1l1_opy_ (u"ࠩࡵࡩࡷࡻ࡮ࡕࡧࡶࡸࡸ࠭ᛐ"): bstack1ll1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࡠࡖࡈࡗ࡙࡙ࠧᛑ"),
  bstack1ll1l1_opy_ (u"ࠫࡦࡶࡰࠨᛒ"): [bstack1ll1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆࡖࡐࡠࡋࡇࠫᛓ"), bstack1ll1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡐࡑࠩᛔ")],
  bstack1ll1l1_opy_ (u"ࠧ࡭ࡱࡪࡐࡪࡼࡥ࡭ࠩᛕ"): bstack1ll1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡔࡆࡎࡣࡑࡕࡇࡍࡇ࡙ࡉࡑ࠭ᛖ"),
  bstack1ll1l1_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ᛗ"): bstack1ll1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄ࡙࡙ࡕࡍࡂࡖࡌࡓࡓ࠭ᛘ"),
  bstack1ll1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨᛙ"): bstack1ll1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡒࡆࡘࡋࡒࡗࡃࡅࡍࡑࡏࡔ࡚ࠩᛚ"),
  bstack1ll1l1_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪᛛ"): bstack1ll1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡖࡔࡅࡓࡘࡉࡁࡍࡇࠪᛜ")
}
bstack1l11l11l1l_opy_ = {
  bstack1ll1l1_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪᛝ"): [bstack1ll1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡷࡶࡩࡷࡥ࡮ࡢ࡯ࡨࠫᛞ"), bstack1ll1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡸࡷࡪࡸࡎࡢ࡯ࡨࠫᛟ")],
  bstack1ll1l1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧᛠ"): [bstack1ll1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶࡣࡰ࡫ࡹࠨᛡ"), bstack1ll1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨᛢ")],
  bstack1ll1l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪᛣ"): bstack1ll1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪᛤ"),
  bstack1ll1l1_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧᛥ"): bstack1ll1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧᛦ"),
  bstack1ll1l1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ᛧ"): bstack1ll1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ᛨ"),
  bstack1ll1l1_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭ᛩ"): [bstack1ll1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡰࡱࡲࠪᛪ"), bstack1ll1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ᛫")],
  bstack1ll1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭᛬"): bstack1ll1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳࡨࡧ࡬ࠨ᛭"),
  bstack1ll1l1_opy_ (u"ࠫࡷ࡫ࡲࡶࡰࡗࡩࡸࡺࡳࠨᛮ"): bstack1ll1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡷ࡫ࡲࡶࡰࡗࡩࡸࡺࡳࠨᛯ"),
  bstack1ll1l1_opy_ (u"࠭ࡡࡱࡲࠪᛰ"): bstack1ll1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡱࡲࠪᛱ"),
  bstack1ll1l1_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪᛲ"): bstack1ll1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪᛳ"),
  bstack1ll1l1_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᛴ"): bstack1ll1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᛵ")
}
bstack1l1l1ll11_opy_ = {
  bstack1ll1l1_opy_ (u"ࠬࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨᛶ"): bstack1ll1l1_opy_ (u"࠭࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠪᛷ"),
  bstack1ll1l1_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩᛸ"): [bstack1ll1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡡࡹࡩࡷࡹࡩࡰࡰࠪ᛹"), bstack1ll1l1_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ᛺")],
  bstack1ll1l1_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ᛻"): bstack1ll1l1_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ᛼"),
  bstack1ll1l1_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠩ᛽"): bstack1ll1l1_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪ࠭᛾"),
  bstack1ll1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬ᛿"): [bstack1ll1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࠩᜀ"), bstack1ll1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡲࡦࡳࡥࠨᜁ")],
  bstack1ll1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫᜂ"): bstack1ll1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᜃ"),
  bstack1ll1l1_opy_ (u"ࠬࡸࡥࡢ࡮ࡐࡳࡧ࡯࡬ࡦࠩᜄ"): bstack1ll1l1_opy_ (u"࠭ࡲࡦࡣ࡯ࡣࡲࡵࡢࡪ࡮ࡨࠫᜅ"),
  bstack1ll1l1_opy_ (u"ࠧࡢࡲࡳ࡭ࡺࡳࡖࡦࡴࡶ࡭ࡴࡴࠧᜆ"): [bstack1ll1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡲࡳ࡭ࡺࡳ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᜇ"), bstack1ll1l1_opy_ (u"ࠩࡤࡴࡵ࡯ࡵ࡮ࡡࡹࡩࡷࡹࡩࡰࡰࠪᜈ")],
  bstack1ll1l1_opy_ (u"ࠪࡥࡨࡩࡥࡱࡶࡌࡲࡸ࡫ࡣࡶࡴࡨࡇࡪࡸࡴࡴࠩᜉ"): [bstack1ll1l1_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡗࡸࡲࡃࡦࡴࡷࡷࠬᜊ"), bstack1ll1l1_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡘࡹ࡬ࡄࡧࡵࡸࠬᜋ")]
}
bstack1l11ll1l1_opy_ = [
  bstack1ll1l1_opy_ (u"࠭ࡡࡤࡥࡨࡴࡹࡏ࡮ࡴࡧࡦࡹࡷ࡫ࡃࡦࡴࡷࡷࠬᜌ"),
  bstack1ll1l1_opy_ (u"ࠧࡱࡣࡪࡩࡑࡵࡡࡥࡕࡷࡶࡦࡺࡥࡨࡻࠪᜍ"),
  bstack1ll1l1_opy_ (u"ࠨࡲࡵࡳࡽࡿࠧᜎ"),
  bstack1ll1l1_opy_ (u"ࠩࡶࡩࡹ࡝ࡩ࡯ࡦࡲࡻࡗ࡫ࡣࡵࠩᜏ"),
  bstack1ll1l1_opy_ (u"ࠪࡸ࡮ࡳࡥࡰࡷࡷࡷࠬᜐ"),
  bstack1ll1l1_opy_ (u"ࠫࡸࡺࡲࡪࡥࡷࡊ࡮ࡲࡥࡊࡰࡷࡩࡷࡧࡣࡵࡣࡥ࡭ࡱ࡯ࡴࡺࠩᜑ"),
  bstack1ll1l1_opy_ (u"ࠬࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡑࡴࡲࡱࡵࡺࡂࡦࡪࡤࡺ࡮ࡵࡲࠨᜒ"),
  bstack1ll1l1_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᜓ"),
  bstack1ll1l1_opy_ (u"ࠧ࡮ࡱࡽ࠾࡫࡯ࡲࡦࡨࡲࡼࡔࡶࡴࡪࡱࡱࡷ᜔ࠬ"),
  bstack1ll1l1_opy_ (u"ࠨ࡯ࡶ࠾ࡪࡪࡧࡦࡑࡳࡸ࡮ࡵ࡮ࡴ᜕ࠩ"),
  bstack1ll1l1_opy_ (u"ࠩࡶࡩ࠿࡯ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨ᜖"),
  bstack1ll1l1_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫࠱ࡳࡵࡺࡩࡰࡰࡶࠫ᜗"),
]
bstack11l1l11ll1_opy_ = [
  bstack1ll1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ᜘"),
  bstack1ll1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ᜙"),
  bstack1ll1l1_opy_ (u"࠭࡬ࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬ᜚"),
  bstack1ll1l1_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ᜛"),
  bstack1ll1l1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ᜜"),
  bstack1ll1l1_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫ᜝"),
  bstack1ll1l1_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭᜞"),
  bstack1ll1l1_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨᜟ"),
  bstack1ll1l1_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨᜠ"),
  bstack1ll1l1_opy_ (u"࠭ࡴࡦࡵࡷࡇࡴࡴࡴࡦࡺࡷࡓࡵࡺࡩࡰࡰࡶࠫᜡ"),
  bstack1ll1l1_opy_ (u"ࠧࡵࡧࡶࡸࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫᜢ"),
  bstack1ll1l1_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡗࡣࡵ࡭ࡦࡨ࡬ࡦࡵࠪᜣ"),
  bstack1ll1l1_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡖࡤ࡫ࠬᜤ"),
  bstack1ll1l1_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᜥ"),
  bstack1ll1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ᜦ"),
  bstack1ll1l1_opy_ (u"ࠬࡸࡥࡳࡷࡱࡘࡪࡹࡴࡴࠩᜧ"),
  bstack1ll1l1_opy_ (u"࠭ࡃࡖࡕࡗࡓࡒࡥࡔࡂࡉࡢ࠵ࠬᜨ"),
  bstack1ll1l1_opy_ (u"ࠧࡄࡗࡖࡘࡔࡓ࡟ࡕࡃࡊࡣ࠷࠭ᜩ"),
  bstack1ll1l1_opy_ (u"ࠨࡅࡘࡗ࡙ࡕࡍࡠࡖࡄࡋࡤ࠹ࠧᜪ"),
  bstack1ll1l1_opy_ (u"ࠩࡆ࡙ࡘ࡚ࡏࡎࡡࡗࡅࡌࡥ࠴ࠨᜫ"),
  bstack1ll1l1_opy_ (u"ࠪࡇ࡚࡙ࡔࡐࡏࡢࡘࡆࡍ࡟࠶ࠩᜬ"),
  bstack1ll1l1_opy_ (u"ࠫࡈ࡛ࡓࡕࡑࡐࡣ࡙ࡇࡇࡠ࠸ࠪᜭ"),
  bstack1ll1l1_opy_ (u"ࠬࡉࡕࡔࡖࡒࡑࡤ࡚ࡁࡈࡡ࠺ࠫᜮ"),
  bstack1ll1l1_opy_ (u"࠭ࡃࡖࡕࡗࡓࡒࡥࡔࡂࡉࡢ࠼ࠬᜯ"),
  bstack1ll1l1_opy_ (u"ࠧࡄࡗࡖࡘࡔࡓ࡟ࡕࡃࡊࡣ࠾࠭ᜰ"),
  bstack1ll1l1_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧᜱ"),
  bstack1ll1l1_opy_ (u"ࠩࡳࡩࡷࡩࡹࡐࡲࡷ࡭ࡴࡴࡳࠨᜲ"),
  bstack1ll1l1_opy_ (u"ࠪࡴࡪࡸࡣࡺࡅࡤࡴࡹࡻࡲࡦࡏࡲࡨࡪ࠭ᜳ"),
  bstack1ll1l1_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡆࡻࡴࡰࡅࡤࡴࡹࡻࡲࡦࡎࡲ࡫ࡸ᜴࠭"),
  bstack1ll1l1_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩ᜵"),
  bstack1ll1l1_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ᜶")
]
bstack11ll1l1ll1l_opy_ = [
  bstack1ll1l1_opy_ (u"ࠧࡶࡲ࡯ࡳࡦࡪࡍࡦࡦ࡬ࡥࠬ᜷"),
  bstack1ll1l1_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ᜸"),
  bstack1ll1l1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬ᜹"),
  bstack1ll1l1_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ᜺"),
  bstack1ll1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡒࡵ࡭ࡴࡸࡩࡵࡻࠪ᜻"),
  bstack1ll1l1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ᜼"),
  bstack1ll1l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨ࡙ࡧࡧࠨ᜽"),
  bstack1ll1l1_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬ᜾"),
  bstack1ll1l1_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯࡙ࡩࡷࡹࡩࡰࡰࠪ᜿"),
  bstack1ll1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧᝀ"),
  bstack1ll1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫᝁ"),
  bstack1ll1l1_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࠪᝂ"),
  bstack1ll1l1_opy_ (u"ࠬࡵࡳࠨᝃ"),
  bstack1ll1l1_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩᝄ"),
  bstack1ll1l1_opy_ (u"ࠧࡩࡱࡶࡸࡸ࠭ᝅ"),
  bstack1ll1l1_opy_ (u"ࠨࡣࡸࡸࡴ࡝ࡡࡪࡶࠪᝆ"),
  bstack1ll1l1_opy_ (u"ࠩࡵࡩ࡬࡯࡯࡯ࠩᝇ"),
  bstack1ll1l1_opy_ (u"ࠪࡸ࡮ࡳࡥࡻࡱࡱࡩࠬᝈ"),
  bstack1ll1l1_opy_ (u"ࠫࡲࡧࡣࡩ࡫ࡱࡩࠬᝉ"),
  bstack1ll1l1_opy_ (u"ࠬࡸࡥࡴࡱ࡯ࡹࡹ࡯࡯࡯ࠩᝊ"),
  bstack1ll1l1_opy_ (u"࠭ࡩࡥ࡮ࡨࡘ࡮ࡳࡥࡰࡷࡷࠫᝋ"),
  bstack1ll1l1_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡏࡳ࡫ࡨࡲࡹࡧࡴࡪࡱࡱࠫᝌ"),
  bstack1ll1l1_opy_ (u"ࠨࡸ࡬ࡨࡪࡵࠧᝍ"),
  bstack1ll1l1_opy_ (u"ࠩࡱࡳࡕࡧࡧࡦࡎࡲࡥࡩ࡚ࡩ࡮ࡧࡲࡹࡹ࠭ᝎ"),
  bstack1ll1l1_opy_ (u"ࠪࡦ࡫ࡩࡡࡤࡪࡨࠫᝏ"),
  bstack1ll1l1_opy_ (u"ࠫࡩ࡫ࡢࡶࡩࠪᝐ"),
  bstack1ll1l1_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡘࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡴࠩᝑ"),
  bstack1ll1l1_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲ࡙ࡥ࡯ࡦࡎࡩࡾࡹࠧᝒ"),
  bstack1ll1l1_opy_ (u"ࠧࡳࡧࡤࡰࡒࡵࡢࡪ࡮ࡨࠫᝓ"),
  bstack1ll1l1_opy_ (u"ࠨࡰࡲࡔ࡮ࡶࡥ࡭࡫ࡱࡩࠬ᝔"),
  bstack1ll1l1_opy_ (u"ࠩࡦ࡬ࡪࡩ࡫ࡖࡔࡏࠫ᝕"),
  bstack1ll1l1_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ᝖"),
  bstack1ll1l1_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡇࡴࡵ࡫ࡪࡧࡶࠫ᝗"),
  bstack1ll1l1_opy_ (u"ࠬࡩࡡࡱࡶࡸࡶࡪࡉࡲࡢࡵ࡫ࠫ᝘"),
  bstack1ll1l1_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪ᝙"),
  bstack1ll1l1_opy_ (u"ࠧࡢࡲࡳ࡭ࡺࡳࡖࡦࡴࡶ࡭ࡴࡴࠧ᝚"),
  bstack1ll1l1_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࡛࡫ࡲࡴ࡫ࡲࡲࠬ᝛"),
  bstack1ll1l1_opy_ (u"ࠩࡱࡳࡇࡲࡡ࡯࡭ࡓࡳࡱࡲࡩ࡯ࡩࠪ᝜"),
  bstack1ll1l1_opy_ (u"ࠪࡱࡦࡹ࡫ࡔࡧࡱࡨࡐ࡫ࡹࡴࠩ᝝"),
  bstack1ll1l1_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡐࡴ࡭ࡳࠨ᝞"),
  bstack1ll1l1_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡎࡪࠧ᝟"),
  bstack1ll1l1_opy_ (u"࠭ࡤࡦࡦ࡬ࡧࡦࡺࡥࡥࡆࡨࡺ࡮ࡩࡥࠨᝠ"),
  bstack1ll1l1_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡐࡢࡴࡤࡱࡸ࠭ᝡ"),
  bstack1ll1l1_opy_ (u"ࠨࡲ࡫ࡳࡳ࡫ࡎࡶ࡯ࡥࡩࡷ࠭ᝢ"),
  bstack1ll1l1_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡏࡳ࡬ࡹࠧᝣ"),
  bstack1ll1l1_opy_ (u"ࠪࡲࡪࡺࡷࡰࡴ࡮ࡐࡴ࡭ࡳࡐࡲࡷ࡭ࡴࡴࡳࠨᝤ"),
  bstack1ll1l1_opy_ (u"ࠫࡨࡵ࡮ࡴࡱ࡯ࡩࡑࡵࡧࡴࠩᝥ"),
  bstack1ll1l1_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬᝦ"),
  bstack1ll1l1_opy_ (u"࠭ࡡࡱࡲ࡬ࡹࡲࡒ࡯ࡨࡵࠪᝧ"),
  bstack1ll1l1_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡂࡪࡱࡰࡩࡹࡸࡩࡤࠩᝨ"),
  bstack1ll1l1_opy_ (u"ࠨࡸ࡬ࡨࡪࡵࡖ࠳ࠩᝩ"),
  bstack1ll1l1_opy_ (u"ࠩࡰ࡭ࡩ࡙ࡥࡴࡵ࡬ࡳࡳࡏ࡮ࡴࡶࡤࡰࡱࡇࡰࡱࡵࠪᝪ"),
  bstack1ll1l1_opy_ (u"ࠪࡩࡸࡶࡲࡦࡵࡶࡳࡘ࡫ࡲࡷࡧࡵࠫᝫ"),
  bstack1ll1l1_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡒ࡯ࡨࡵࠪᝬ"),
  bstack1ll1l1_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࡃࡥࡲࠪ᝭"),
  bstack1ll1l1_opy_ (u"࠭ࡴࡦ࡮ࡨࡱࡪࡺࡲࡺࡎࡲ࡫ࡸ࠭ᝮ"),
  bstack1ll1l1_opy_ (u"ࠧࡴࡻࡱࡧ࡙࡯࡭ࡦ࡙࡬ࡸ࡭ࡔࡔࡑࠩᝯ"),
  bstack1ll1l1_opy_ (u"ࠨࡩࡨࡳࡑࡵࡣࡢࡶ࡬ࡳࡳ࠭ᝰ"),
  bstack1ll1l1_opy_ (u"ࠩࡪࡴࡸࡒ࡯ࡤࡣࡷ࡭ࡴࡴࠧ᝱"),
  bstack1ll1l1_opy_ (u"ࠪࡲࡪࡺࡷࡰࡴ࡮ࡔࡷࡵࡦࡪ࡮ࡨࠫᝲ"),
  bstack1ll1l1_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡒࡪࡺࡷࡰࡴ࡮ࠫᝳ"),
  bstack1ll1l1_opy_ (u"ࠬ࡬࡯ࡳࡥࡨࡇ࡭ࡧ࡮ࡨࡧࡍࡥࡷ࠭᝴"),
  bstack1ll1l1_opy_ (u"࠭ࡸ࡮ࡵࡍࡥࡷ࠭᝵"),
  bstack1ll1l1_opy_ (u"ࠧࡹ࡯ࡻࡎࡦࡸࠧ᝶"),
  bstack1ll1l1_opy_ (u"ࠨ࡯ࡤࡷࡰࡉ࡯࡮࡯ࡤࡲࡩࡹࠧ᝷"),
  bstack1ll1l1_opy_ (u"ࠩࡰࡥࡸࡱࡂࡢࡵ࡬ࡧࡆࡻࡴࡩࠩ᝸"),
  bstack1ll1l1_opy_ (u"ࠪࡻࡸࡒ࡯ࡤࡣ࡯ࡗࡺࡶࡰࡰࡴࡷࠫ᝹"),
  bstack1ll1l1_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡈࡵࡲࡴࡔࡨࡷࡹࡸࡩࡤࡶ࡬ࡳࡳࡹࠧ᝺"),
  bstack1ll1l1_opy_ (u"ࠬࡧࡰࡱࡘࡨࡶࡸ࡯࡯࡯ࠩ᝻"),
  bstack1ll1l1_opy_ (u"࠭ࡡࡤࡥࡨࡴࡹࡏ࡮ࡴࡧࡦࡹࡷ࡫ࡃࡦࡴࡷࡷࠬ᝼"),
  bstack1ll1l1_opy_ (u"ࠧࡳࡧࡶ࡭࡬ࡴࡁࡱࡲࠪ᝽"),
  bstack1ll1l1_opy_ (u"ࠨࡦ࡬ࡷࡦࡨ࡬ࡦࡃࡱ࡭ࡲࡧࡴࡪࡱࡱࡷࠬ᝾"),
  bstack1ll1l1_opy_ (u"ࠩࡦࡥࡳࡧࡲࡺࠩ᝿"),
  bstack1ll1l1_opy_ (u"ࠪࡪ࡮ࡸࡥࡧࡱࡻࠫក"),
  bstack1ll1l1_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫខ"),
  bstack1ll1l1_opy_ (u"ࠬ࡯ࡥࠨគ"),
  bstack1ll1l1_opy_ (u"࠭ࡥࡥࡩࡨࠫឃ"),
  bstack1ll1l1_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࠧង"),
  bstack1ll1l1_opy_ (u"ࠨࡳࡸࡩࡺ࡫ࠧច"),
  bstack1ll1l1_opy_ (u"ࠩ࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫឆ"),
  bstack1ll1l1_opy_ (u"ࠪࡥࡵࡶࡓࡵࡱࡵࡩࡈࡵ࡮ࡧ࡫ࡪࡹࡷࡧࡴࡪࡱࡱࠫជ"),
  bstack1ll1l1_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡇࡦࡳࡥࡳࡣࡌࡱࡦ࡭ࡥࡊࡰ࡭ࡩࡨࡺࡩࡰࡰࠪឈ"),
  bstack1ll1l1_opy_ (u"ࠬࡴࡥࡵࡹࡲࡶࡰࡒ࡯ࡨࡵࡈࡼࡨࡲࡵࡥࡧࡋࡳࡸࡺࡳࠨញ"),
  bstack1ll1l1_opy_ (u"࠭࡮ࡦࡶࡺࡳࡷࡱࡌࡰࡩࡶࡍࡳࡩ࡬ࡶࡦࡨࡌࡴࡹࡴࡴࠩដ"),
  bstack1ll1l1_opy_ (u"ࠧࡶࡲࡧࡥࡹ࡫ࡁࡱࡲࡖࡩࡹࡺࡩ࡯ࡩࡶࠫឋ"),
  bstack1ll1l1_opy_ (u"ࠨࡴࡨࡷࡪࡸࡶࡦࡆࡨࡺ࡮ࡩࡥࠨឌ"),
  bstack1ll1l1_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩឍ"),
  bstack1ll1l1_opy_ (u"ࠪࡷࡪࡴࡤࡌࡧࡼࡷࠬណ"),
  bstack1ll1l1_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡔࡦࡹࡳࡤࡱࡧࡩࠬត"),
  bstack1ll1l1_opy_ (u"ࠬࡻࡰࡥࡣࡷࡩࡎࡵࡳࡅࡧࡹ࡭ࡨ࡫ࡓࡦࡶࡷ࡭ࡳ࡭ࡳࠨថ"),
  bstack1ll1l1_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡇࡵࡥ࡫ࡲࡍࡳࡰࡥࡤࡶ࡬ࡳࡳ࠭ទ"),
  bstack1ll1l1_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡁࡱࡲ࡯ࡩࡕࡧࡹࠨធ"),
  bstack1ll1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࠩន"),
  bstack1ll1l1_opy_ (u"ࠩࡺࡨ࡮ࡵࡓࡦࡴࡹ࡭ࡨ࡫ࠧប"),
  bstack1ll1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬផ"),
  bstack1ll1l1_opy_ (u"ࠫࡵࡸࡥࡷࡧࡱࡸࡈࡸ࡯ࡴࡵࡖ࡭ࡹ࡫ࡔࡳࡣࡦ࡯࡮ࡴࡧࠨព"),
  bstack1ll1l1_opy_ (u"ࠬ࡮ࡩࡨࡪࡆࡳࡳࡺࡲࡢࡵࡷࠫភ"),
  bstack1ll1l1_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡖࡲࡦࡨࡨࡶࡪࡴࡣࡦࡵࠪម"),
  bstack1ll1l1_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡓࡪ࡯ࠪយ"),
  bstack1ll1l1_opy_ (u"ࠨࡵ࡬ࡱࡔࡶࡴࡪࡱࡱࡷࠬរ"),
  bstack1ll1l1_opy_ (u"ࠩࡵࡩࡲࡵࡶࡦࡋࡒࡗࡆࡶࡰࡔࡧࡷࡸ࡮ࡴࡧࡴࡎࡲࡧࡦࡲࡩࡻࡣࡷ࡭ࡴࡴࠧល"),
  bstack1ll1l1_opy_ (u"ࠪ࡬ࡴࡹࡴࡏࡣࡰࡩࠬវ"),
  bstack1ll1l1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ឝ"),
  bstack1ll1l1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࠧឞ"),
  bstack1ll1l1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠬស"),
  bstack1ll1l1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩហ"),
  bstack1ll1l1_opy_ (u"ࠨࡲࡤ࡫ࡪࡒ࡯ࡢࡦࡖࡸࡷࡧࡴࡦࡩࡼࠫឡ"),
  bstack1ll1l1_opy_ (u"ࠩࡳࡶࡴࡾࡹࠨអ"),
  bstack1ll1l1_opy_ (u"ࠪࡸ࡮ࡳࡥࡰࡷࡷࡷࠬឣ"),
  bstack1ll1l1_opy_ (u"ࠫࡺࡴࡨࡢࡰࡧࡰࡪࡪࡐࡳࡱࡰࡴࡹࡈࡥࡩࡣࡹ࡭ࡴࡸࠧឤ")
]
bstack1l11lll1l_opy_ = {
  bstack1ll1l1_opy_ (u"ࠬࡼࠧឥ"): bstack1ll1l1_opy_ (u"࠭ࡶࠨឦ"),
  bstack1ll1l1_opy_ (u"ࠧࡧࠩឧ"): bstack1ll1l1_opy_ (u"ࠨࡨࠪឨ"),
  bstack1ll1l1_opy_ (u"ࠩࡩࡳࡷࡩࡥࠨឩ"): bstack1ll1l1_opy_ (u"ࠪࡪࡴࡸࡣࡦࠩឪ"),
  bstack1ll1l1_opy_ (u"ࠫࡴࡴ࡬ࡺࡣࡸࡸࡴࡳࡡࡵࡧࠪឫ"): bstack1ll1l1_opy_ (u"ࠬࡵ࡮࡭ࡻࡄࡹࡹࡵ࡭ࡢࡶࡨࠫឬ"),
  bstack1ll1l1_opy_ (u"࠭ࡦࡰࡴࡦࡩࡱࡵࡣࡢ࡮ࠪឭ"): bstack1ll1l1_opy_ (u"ࠧࡧࡱࡵࡧࡪࡲ࡯ࡤࡣ࡯ࠫឮ"),
  bstack1ll1l1_opy_ (u"ࠨࡲࡵࡳࡽࡿࡨࡰࡵࡷࠫឯ"): bstack1ll1l1_opy_ (u"ࠩࡳࡶࡴࡾࡹࡉࡱࡶࡸࠬឰ"),
  bstack1ll1l1_opy_ (u"ࠪࡴࡷࡵࡸࡺࡲࡲࡶࡹ࠭ឱ"): bstack1ll1l1_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡓࡳࡷࡺࠧឲ"),
  bstack1ll1l1_opy_ (u"ࠬࡶࡲࡰࡺࡼࡹࡸ࡫ࡲࠨឳ"): bstack1ll1l1_opy_ (u"࠭ࡰࡳࡱࡻࡽ࡚ࡹࡥࡳࠩ឴"),
  bstack1ll1l1_opy_ (u"ࠧࡱࡴࡲࡼࡾࡶࡡࡴࡵࠪ឵"): bstack1ll1l1_opy_ (u"ࠨࡲࡵࡳࡽࡿࡐࡢࡵࡶࠫា"),
  bstack1ll1l1_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡱࡴࡲࡼࡾ࡮࡯ࡴࡶࠪិ"): bstack1ll1l1_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡒࡵࡳࡽࡿࡈࡰࡵࡷࠫី"),
  bstack1ll1l1_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡳࡶࡴࡾࡹࡱࡱࡵࡸࠬឹ"): bstack1ll1l1_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡔࡷࡵࡸࡺࡒࡲࡶࡹ࠭ឺ"),
  bstack1ll1l1_opy_ (u"࠭࡬ࡰࡥࡤࡰࡵࡸ࡯ࡹࡻࡸࡷࡪࡸࠧុ"): bstack1ll1l1_opy_ (u"ࠧ࠮࡮ࡲࡧࡦࡲࡐࡳࡱࡻࡽ࡚ࡹࡥࡳࠩូ"),
  bstack1ll1l1_opy_ (u"ࠨ࠯࡯ࡳࡨࡧ࡬ࡱࡴࡲࡼࡾࡻࡳࡦࡴࠪួ"): bstack1ll1l1_opy_ (u"ࠩ࠰ࡰࡴࡩࡡ࡭ࡒࡵࡳࡽࡿࡕࡴࡧࡵࠫើ"),
  bstack1ll1l1_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡲࡵࡳࡽࡿࡰࡢࡵࡶࠫឿ"): bstack1ll1l1_opy_ (u"ࠫ࠲ࡲ࡯ࡤࡣ࡯ࡔࡷࡵࡸࡺࡒࡤࡷࡸ࠭ៀ"),
  bstack1ll1l1_opy_ (u"ࠬ࠳࡬ࡰࡥࡤࡰࡵࡸ࡯ࡹࡻࡳࡥࡸࡹࠧេ"): bstack1ll1l1_opy_ (u"࠭࠭࡭ࡱࡦࡥࡱࡖࡲࡰࡺࡼࡔࡦࡹࡳࠨែ"),
  bstack1ll1l1_opy_ (u"ࠧࡣ࡫ࡱࡥࡷࡿࡰࡢࡶ࡫ࠫៃ"): bstack1ll1l1_opy_ (u"ࠨࡤ࡬ࡲࡦࡸࡹࡱࡣࡷ࡬ࠬោ"),
  bstack1ll1l1_opy_ (u"ࠩࡳࡥࡨ࡬ࡩ࡭ࡧࠪៅ"): bstack1ll1l1_opy_ (u"ࠪ࠱ࡵࡧࡣ࠮ࡨ࡬ࡰࡪ࠭ំ"),
  bstack1ll1l1_opy_ (u"ࠫࡵࡧࡣ࠮ࡨ࡬ࡰࡪ࠭ះ"): bstack1ll1l1_opy_ (u"ࠬ࠳ࡰࡢࡥ࠰ࡪ࡮ࡲࡥࠨៈ"),
  bstack1ll1l1_opy_ (u"࠭࠭ࡱࡣࡦ࠱࡫࡯࡬ࡦࠩ៉"): bstack1ll1l1_opy_ (u"ࠧ࠮ࡲࡤࡧ࠲࡬ࡩ࡭ࡧࠪ៊"),
  bstack1ll1l1_opy_ (u"ࠨ࡮ࡲ࡫࡫࡯࡬ࡦࠩ់"): bstack1ll1l1_opy_ (u"ࠩ࡯ࡳ࡬࡬ࡩ࡭ࡧࠪ៌"),
  bstack1ll1l1_opy_ (u"ࠪࡰࡴࡩࡡ࡭࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ៍"): bstack1ll1l1_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭៎"),
  bstack1ll1l1_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱ࠲ࡸࡥࡱࡧࡤࡸࡪࡸࠧ៏"): bstack1ll1l1_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡘࡥࡱࡧࡤࡸࡪࡸࠧ័")
}
bstack11ll1ll1l11_opy_ = bstack1ll1l1_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࡩ࡬ࡸ࡭ࡻࡢ࠯ࡥࡲࡱ࠴ࡶࡥࡳࡥࡼ࠳ࡨࡲࡩ࠰ࡴࡨࡰࡪࡧࡳࡦࡵ࠲ࡰࡦࡺࡥࡴࡶ࠲ࡨࡴࡽ࡮࡭ࡱࡤࡨࠧ៑")
bstack11lll111111_opy_ = bstack1ll1l1_opy_ (u"ࠣ࠱ࡳࡩࡷࡩࡹ࠰ࡪࡨࡥࡱࡺࡨࡤࡪࡨࡧࡰࠨ្")
bstack1llll1ll1_opy_ = bstack1ll1l1_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡩࡩࡹ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡷࡪࡴࡤࡠࡵࡧ࡯ࡤ࡫ࡶࡦࡰࡷࡷࠧ៓")
bstack1l1ll1lll_opy_ = bstack1ll1l1_opy_ (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳࡭ࡻࡢ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡼࡪ࠯ࡩࡷࡥࠫ។")
bstack1lllll1l1_opy_ = bstack1ll1l1_opy_ (u"ࠫ࡭ࡺࡴࡱ࠼࠲࠳࡭ࡻࡢ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠾࠽࠶࠯ࡸࡦ࠲࡬ࡺࡨࠧ៕")
bstack11l1ll111l_opy_ = bstack1ll1l1_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡨࡶࡤ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵࡮ࡦࡺࡷࡣ࡭ࡻࡢࡴࠩ៖")
bstack11lll111ll1_opy_ = {
  bstack1ll1l1_opy_ (u"࠭ࡣࡳ࡫ࡷ࡭ࡨࡧ࡬ࠨៗ"): 50,
  bstack1ll1l1_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭៘"): 40,
  bstack1ll1l1_opy_ (u"ࠨࡹࡤࡶࡳ࡯࡮ࡨࠩ៙"): 30,
  bstack1ll1l1_opy_ (u"ࠩ࡬ࡲ࡫ࡵࠧ៚"): 20,
  bstack1ll1l1_opy_ (u"ࠪࡨࡪࡨࡵࡨࠩ៛"): 10
}
bstack1ll111lll1_opy_ = bstack11lll111ll1_opy_[bstack1ll1l1_opy_ (u"ࠫ࡮ࡴࡦࡰࠩៜ")]
bstack1l1111ll1_opy_ = bstack1ll1l1_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠲ࡶࡹࡵࡪࡲࡲࡦ࡭ࡥ࡯ࡶ࠲ࠫ៝")
bstack1ll1ll11ll_opy_ = bstack1ll1l1_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲ࡶࡹࡵࡪࡲࡲࡦ࡭ࡥ࡯ࡶ࠲ࠫ៞")
bstack111lll1ll_opy_ = bstack1ll1l1_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫࠭ࡱࡻࡷ࡬ࡴࡴࡡࡨࡧࡱࡸ࠴࠭៟")
bstack1l1111l1_opy_ = bstack1ll1l1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴ࠮ࡲࡼࡸ࡭ࡵ࡮ࡢࡩࡨࡲࡹ࠵ࠧ០")
bstack11ll1111ll_opy_ = bstack1ll1l1_opy_ (u"ࠩࡓࡰࡪࡧࡳࡦࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡴࡾࡺࡥࡴࡶࠣࡥࡳࡪࠠࡱࡻࡷࡩࡸࡺ࠭ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠢࡳࡥࡨࡱࡡࡨࡧࡶ࠲ࠥࡦࡰࡪࡲࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤࡵࡿࡴࡦࡵࡷࠤࡵࡿࡴࡦࡵࡷ࠱ࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡦࠧ១")
bstack11ll1l11l11_opy_ = [bstack1ll1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡘࡗࡊࡘࡎࡂࡏࡈࠫ២"), bstack1ll1l1_opy_ (u"ࠫ࡞ࡕࡕࡓࡡࡘࡗࡊࡘࡎࡂࡏࡈࠫ៣")]
bstack11lll1111ll_opy_ = [bstack1ll1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆࡉࡃࡆࡕࡖࡣࡐࡋ࡙ࠨ៤"), bstack1ll1l1_opy_ (u"࡙࠭ࡐࡗࡕࡣࡆࡉࡃࡆࡕࡖࡣࡐࡋ࡙ࠨ៥")]
bstack1ll1ll1l_opy_ = re.compile(bstack1ll1l1_opy_ (u"ࠧ࡟࡝࡟ࡠࡼ࠳࡝ࠬ࠼࠱࠮ࠩ࠭៦"))
bstack1lll11l11l_opy_ = [
  bstack1ll1l1_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡓࡧ࡭ࡦࠩ៧"),
  bstack1ll1l1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠫ៨"),
  bstack1ll1l1_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧ៩"),
  bstack1ll1l1_opy_ (u"ࠫࡳ࡫ࡷࡄࡱࡰࡱࡦࡴࡤࡕ࡫ࡰࡩࡴࡻࡴࠨ៪"),
  bstack1ll1l1_opy_ (u"ࠬࡧࡰࡱࠩ៫"),
  bstack1ll1l1_opy_ (u"࠭ࡵࡥ࡫ࡧࠫ៬"),
  bstack1ll1l1_opy_ (u"ࠧ࡭ࡣࡱ࡫ࡺࡧࡧࡦࠩ៭"),
  bstack1ll1l1_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡥࠨ៮"),
  bstack1ll1l1_opy_ (u"ࠩࡲࡶ࡮࡫࡮ࡵࡣࡷ࡭ࡴࡴࠧ៯"),
  bstack1ll1l1_opy_ (u"ࠪࡥࡺࡺ࡯ࡘࡧࡥࡺ࡮࡫ࡷࠨ៰"),
  bstack1ll1l1_opy_ (u"ࠫࡳࡵࡒࡦࡵࡨࡸࠬ៱"), bstack1ll1l1_opy_ (u"ࠬ࡬ࡵ࡭࡮ࡕࡩࡸ࡫ࡴࠨ៲"),
  bstack1ll1l1_opy_ (u"࠭ࡣ࡭ࡧࡤࡶࡘࡿࡳࡵࡧࡰࡊ࡮ࡲࡥࡴࠩ៳"),
  bstack1ll1l1_opy_ (u"ࠧࡦࡸࡨࡲࡹ࡚ࡩ࡮࡫ࡱ࡫ࡸ࠭៴"),
  bstack1ll1l1_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡑࡧࡵࡪࡴࡸ࡭ࡢࡰࡦࡩࡑࡵࡧࡨ࡫ࡱ࡫ࠬ៵"),
  bstack1ll1l1_opy_ (u"ࠩࡲࡸ࡭࡫ࡲࡂࡲࡳࡷࠬ៶"),
  bstack1ll1l1_opy_ (u"ࠪࡴࡷ࡯࡮ࡵࡒࡤ࡫ࡪ࡙࡯ࡶࡴࡦࡩࡔࡴࡆࡪࡰࡧࡊࡦ࡯࡬ࡶࡴࡨࠫ៷"),
  bstack1ll1l1_opy_ (u"ࠫࡦࡶࡰࡂࡥࡷ࡭ࡻ࡯ࡴࡺࠩ៸"), bstack1ll1l1_opy_ (u"ࠬࡧࡰࡱࡒࡤࡧࡰࡧࡧࡦࠩ៹"), bstack1ll1l1_opy_ (u"࠭ࡡࡱࡲ࡚ࡥ࡮ࡺࡁࡤࡶ࡬ࡺ࡮ࡺࡹࠨ៺"), bstack1ll1l1_opy_ (u"ࠧࡢࡲࡳ࡛ࡦ࡯ࡴࡑࡣࡦ࡯ࡦ࡭ࡥࠨ៻"), bstack1ll1l1_opy_ (u"ࠨࡣࡳࡴ࡜ࡧࡩࡵࡆࡸࡶࡦࡺࡩࡰࡰࠪ៼"),
  bstack1ll1l1_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡔࡨࡥࡩࡿࡔࡪ࡯ࡨࡳࡺࡺࠧ៽"),
  bstack1ll1l1_opy_ (u"ࠪࡥࡱࡲ࡯ࡸࡖࡨࡷࡹࡖࡡࡤ࡭ࡤ࡫ࡪࡹࠧ៾"),
  bstack1ll1l1_opy_ (u"ࠫࡦࡴࡤࡳࡱ࡬ࡨࡈࡵࡶࡦࡴࡤ࡫ࡪ࠭៿"), bstack1ll1l1_opy_ (u"ࠬࡧ࡮ࡥࡴࡲ࡭ࡩࡉ࡯ࡷࡧࡵࡥ࡬࡫ࡅ࡯ࡦࡌࡲࡹ࡫࡮ࡵࠩ᠀"),
  bstack1ll1l1_opy_ (u"࠭ࡡ࡯ࡦࡵࡳ࡮ࡪࡄࡦࡸ࡬ࡧࡪࡘࡥࡢࡦࡼࡘ࡮ࡳࡥࡰࡷࡷࠫ᠁"),
  bstack1ll1l1_opy_ (u"ࠧࡢࡦࡥࡔࡴࡸࡴࠨ᠂"),
  bstack1ll1l1_opy_ (u"ࠨࡣࡱࡨࡷࡵࡩࡥࡆࡨࡺ࡮ࡩࡥࡔࡱࡦ࡯ࡪࡺࠧ᠃"),
  bstack1ll1l1_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࡌࡲࡸࡺࡡ࡭࡮ࡗ࡭ࡲ࡫࡯ࡶࡶࠪ᠄"),
  bstack1ll1l1_opy_ (u"ࠪࡥࡳࡪࡲࡰ࡫ࡧࡍࡳࡹࡴࡢ࡮࡯ࡔࡦࡺࡨࠨ᠅"),
  bstack1ll1l1_opy_ (u"ࠫࡦࡼࡤࠨ᠆"), bstack1ll1l1_opy_ (u"ࠬࡧࡶࡥࡎࡤࡹࡳࡩࡨࡕ࡫ࡰࡩࡴࡻࡴࠨ᠇"), bstack1ll1l1_opy_ (u"࠭ࡡࡷࡦࡕࡩࡦࡪࡹࡕ࡫ࡰࡩࡴࡻࡴࠨ᠈"), bstack1ll1l1_opy_ (u"ࠧࡢࡸࡧࡅࡷ࡭ࡳࠨ᠉"),
  bstack1ll1l1_opy_ (u"ࠨࡷࡶࡩࡐ࡫ࡹࡴࡶࡲࡶࡪ࠭᠊"), bstack1ll1l1_opy_ (u"ࠩ࡮ࡩࡾࡹࡴࡰࡴࡨࡔࡦࡺࡨࠨ᠋"), bstack1ll1l1_opy_ (u"ࠪ࡯ࡪࡿࡳࡵࡱࡵࡩࡕࡧࡳࡴࡹࡲࡶࡩ࠭᠌"),
  bstack1ll1l1_opy_ (u"ࠫࡰ࡫ࡹࡂ࡮࡬ࡥࡸ࠭᠍"), bstack1ll1l1_opy_ (u"ࠬࡱࡥࡺࡒࡤࡷࡸࡽ࡯ࡳࡦࠪ᠎"),
  bstack1ll1l1_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡪࡲࡪࡸࡨࡶࡊࡾࡥࡤࡷࡷࡥࡧࡲࡥࠨ᠏"), bstack1ll1l1_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡤࡳ࡫ࡹࡩࡷࡇࡲࡨࡵࠪ᠐"), bstack1ll1l1_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡥࡴ࡬ࡺࡪࡸࡅࡹࡧࡦࡹࡹࡧࡢ࡭ࡧࡇ࡭ࡷ࠭᠑"), bstack1ll1l1_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡦࡵ࡭ࡻ࡫ࡲࡄࡪࡵࡳࡲ࡫ࡍࡢࡲࡳ࡭ࡳ࡭ࡆࡪ࡮ࡨࠫ᠒"), bstack1ll1l1_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡧࡶ࡮ࡼࡥࡳࡗࡶࡩࡘࡿࡳࡵࡧࡰࡉࡽ࡫ࡣࡶࡶࡤࡦࡱ࡫ࠧ᠓"),
  bstack1ll1l1_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡨࡷ࡯ࡶࡦࡴࡓࡳࡷࡺࠧ᠔"), bstack1ll1l1_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡩࡸࡩࡷࡧࡵࡔࡴࡸࡴࡴࠩ᠕"),
  bstack1ll1l1_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡪࡲࡪࡸࡨࡶࡉ࡯ࡳࡢࡤ࡯ࡩࡇࡻࡩ࡭ࡦࡆ࡬ࡪࡩ࡫ࠨ᠖"),
  bstack1ll1l1_opy_ (u"ࠧࡢࡷࡷࡳ࡜࡫ࡢࡷ࡫ࡨࡻ࡙࡯࡭ࡦࡱࡸࡸࠬ᠗"),
  bstack1ll1l1_opy_ (u"ࠨ࡫ࡱࡸࡪࡴࡴࡂࡥࡷ࡭ࡴࡴࠧ᠘"), bstack1ll1l1_opy_ (u"ࠩ࡬ࡲࡹ࡫࡮ࡵࡅࡤࡸࡪ࡭࡯ࡳࡻࠪ᠙"), bstack1ll1l1_opy_ (u"ࠪ࡭ࡳࡺࡥ࡯ࡶࡉࡰࡦ࡭ࡳࠨ᠚"), bstack1ll1l1_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡥࡱࡏ࡮ࡵࡧࡱࡸࡆࡸࡧࡶ࡯ࡨࡲࡹࡹࠧ᠛"),
  bstack1ll1l1_opy_ (u"ࠬࡪ࡯࡯ࡶࡖࡸࡴࡶࡁࡱࡲࡒࡲࡗ࡫ࡳࡦࡶࠪ᠜"),
  bstack1ll1l1_opy_ (u"࠭ࡵ࡯࡫ࡦࡳࡩ࡫ࡋࡦࡻࡥࡳࡦࡸࡤࠨ᠝"), bstack1ll1l1_opy_ (u"ࠧࡳࡧࡶࡩࡹࡑࡥࡺࡤࡲࡥࡷࡪࠧ᠞"),
  bstack1ll1l1_opy_ (u"ࠨࡰࡲࡗ࡮࡭࡮ࠨ᠟"),
  bstack1ll1l1_opy_ (u"ࠩ࡬࡫ࡳࡵࡲࡦࡗࡱ࡭ࡲࡶ࡯ࡳࡶࡤࡲࡹ࡜ࡩࡦࡹࡶࠫᠠ"),
  bstack1ll1l1_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨࡅࡳࡪࡲࡰ࡫ࡧ࡛ࡦࡺࡣࡩࡧࡵࡷࠬᠡ"),
  bstack1ll1l1_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᠢ"),
  bstack1ll1l1_opy_ (u"ࠬࡸࡥࡤࡴࡨࡥࡹ࡫ࡃࡩࡴࡲࡱࡪࡊࡲࡪࡸࡨࡶࡘ࡫ࡳࡴ࡫ࡲࡲࡸ࠭ᠣ"),
  bstack1ll1l1_opy_ (u"࠭࡮ࡢࡶ࡬ࡺࡪ࡝ࡥࡣࡕࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠬᠤ"),
  bstack1ll1l1_opy_ (u"ࠧࡢࡰࡧࡶࡴ࡯ࡤࡔࡥࡵࡩࡪࡴࡳࡩࡱࡷࡔࡦࡺࡨࠨᠥ"),
  bstack1ll1l1_opy_ (u"ࠨࡰࡨࡸࡼࡵࡲ࡬ࡕࡳࡩࡪࡪࠧᠦ"),
  bstack1ll1l1_opy_ (u"ࠩࡪࡴࡸࡋ࡮ࡢࡤ࡯ࡩࡩ࠭ᠧ"),
  bstack1ll1l1_opy_ (u"ࠪ࡭ࡸࡎࡥࡢࡦ࡯ࡩࡸࡹࠧᠨ"),
  bstack1ll1l1_opy_ (u"ࠫࡦࡪࡢࡆࡺࡨࡧ࡙࡯࡭ࡦࡱࡸࡸࠬᠩ"),
  bstack1ll1l1_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡩࡘࡩࡲࡪࡲࡷࠫᠪ"),
  bstack1ll1l1_opy_ (u"࠭ࡳ࡬࡫ࡳࡈࡪࡼࡩࡤࡧࡌࡲ࡮ࡺࡩࡢ࡮࡬ࡾࡦࡺࡩࡰࡰࠪᠫ"),
  bstack1ll1l1_opy_ (u"ࠧࡢࡷࡷࡳࡌࡸࡡ࡯ࡶࡓࡩࡷࡳࡩࡴࡵ࡬ࡳࡳࡹࠧᠬ"),
  bstack1ll1l1_opy_ (u"ࠨࡣࡱࡨࡷࡵࡩࡥࡐࡤࡸࡺࡸࡡ࡭ࡑࡵ࡭ࡪࡴࡴࡢࡶ࡬ࡳࡳ࠭ᠭ"),
  bstack1ll1l1_opy_ (u"ࠩࡶࡽࡸࡺࡥ࡮ࡒࡲࡶࡹ࠭ᠮ"),
  bstack1ll1l1_opy_ (u"ࠪࡶࡪࡳ࡯ࡵࡧࡄࡨࡧࡎ࡯ࡴࡶࠪᠯ"),
  bstack1ll1l1_opy_ (u"ࠫࡸࡱࡩࡱࡗࡱࡰࡴࡩ࡫ࠨᠰ"), bstack1ll1l1_opy_ (u"ࠬࡻ࡮࡭ࡱࡦ࡯࡙ࡿࡰࡦࠩᠱ"), bstack1ll1l1_opy_ (u"࠭ࡵ࡯࡮ࡲࡧࡰࡑࡥࡺࠩᠲ"),
  bstack1ll1l1_opy_ (u"ࠧࡢࡷࡷࡳࡑࡧࡵ࡯ࡥ࡫ࠫᠳ"),
  bstack1ll1l1_opy_ (u"ࠨࡵ࡮࡭ࡵࡒ࡯ࡨࡥࡤࡸࡈࡧࡰࡵࡷࡵࡩࠬᠴ"),
  bstack1ll1l1_opy_ (u"ࠩࡸࡲ࡮ࡴࡳࡵࡣ࡯ࡰࡔࡺࡨࡦࡴࡓࡥࡨࡱࡡࡨࡧࡶࠫᠵ"),
  bstack1ll1l1_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨ࡛࡮ࡴࡤࡰࡹࡄࡲ࡮ࡳࡡࡵ࡫ࡲࡲࠬᠶ"),
  bstack1ll1l1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡗࡳࡴࡲࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨᠷ"),
  bstack1ll1l1_opy_ (u"ࠬ࡫࡮ࡧࡱࡵࡧࡪࡇࡰࡱࡋࡱࡷࡹࡧ࡬࡭ࠩᠸ"),
  bstack1ll1l1_opy_ (u"࠭ࡥ࡯ࡵࡸࡶࡪ࡝ࡥࡣࡸ࡬ࡩࡼࡹࡈࡢࡸࡨࡔࡦ࡭ࡥࡴࠩᠹ"), bstack1ll1l1_opy_ (u"ࠧࡸࡧࡥࡺ࡮࡫ࡷࡅࡧࡹࡸࡴࡵ࡬ࡴࡒࡲࡶࡹ࠭ᠺ"), bstack1ll1l1_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡘࡧࡥࡺ࡮࡫ࡷࡅࡧࡷࡥ࡮ࡲࡳࡄࡱ࡯ࡰࡪࡩࡴࡪࡱࡱࠫᠻ"),
  bstack1ll1l1_opy_ (u"ࠩࡵࡩࡲࡵࡴࡦࡃࡳࡴࡸࡉࡡࡤࡪࡨࡐ࡮ࡳࡩࡵࠩᠼ"),
  bstack1ll1l1_opy_ (u"ࠪࡧࡦࡲࡥ࡯ࡦࡤࡶࡋࡵࡲ࡮ࡣࡷࠫᠽ"),
  bstack1ll1l1_opy_ (u"ࠫࡧࡻ࡮ࡥ࡮ࡨࡍࡩ࠭ᠾ"),
  bstack1ll1l1_opy_ (u"ࠬࡲࡡࡶࡰࡦ࡬࡙࡯࡭ࡦࡱࡸࡸࠬᠿ"),
  bstack1ll1l1_opy_ (u"࠭࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࡔࡧࡵࡺ࡮ࡩࡥࡴࡇࡱࡥࡧࡲࡥࡥࠩᡀ"), bstack1ll1l1_opy_ (u"ࠧ࡭ࡱࡦࡥࡹ࡯࡯࡯ࡕࡨࡶࡻ࡯ࡣࡦࡵࡄࡹࡹ࡮࡯ࡳ࡫ࡽࡩࡩ࠭ᡁ"),
  bstack1ll1l1_opy_ (u"ࠨࡣࡸࡸࡴࡇࡣࡤࡧࡳࡸࡆࡲࡥࡳࡶࡶࠫᡂ"), bstack1ll1l1_opy_ (u"ࠩࡤࡹࡹࡵࡄࡪࡵࡰ࡭ࡸࡹࡁ࡭ࡧࡵࡸࡸ࠭ᡃ"),
  bstack1ll1l1_opy_ (u"ࠪࡲࡦࡺࡩࡷࡧࡌࡲࡸࡺࡲࡶ࡯ࡨࡲࡹࡹࡌࡪࡤࠪᡄ"),
  bstack1ll1l1_opy_ (u"ࠫࡳࡧࡴࡪࡸࡨ࡛ࡪࡨࡔࡢࡲࠪᡅ"),
  bstack1ll1l1_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭ࡎࡴࡩࡵ࡫ࡤࡰ࡚ࡸ࡬ࠨᡆ"), bstack1ll1l1_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮ࡇ࡬࡭ࡱࡺࡔࡴࡶࡵࡱࡵࠪᡇ"), bstack1ll1l1_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࡉࡨࡰࡲࡶࡪࡌࡲࡢࡷࡧ࡛ࡦࡸ࡮ࡪࡰࡪࠫᡈ"), bstack1ll1l1_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࡐࡲࡨࡲࡑ࡯࡮࡬ࡵࡌࡲࡇࡧࡣ࡬ࡩࡵࡳࡺࡴࡤࠨᡉ"),
  bstack1ll1l1_opy_ (u"ࠩ࡮ࡩࡪࡶࡋࡦࡻࡆ࡬ࡦ࡯࡮ࡴࠩᡊ"),
  bstack1ll1l1_opy_ (u"ࠪࡰࡴࡩࡡ࡭࡫ࡽࡥࡧࡲࡥࡔࡶࡵ࡭ࡳ࡭ࡳࡅ࡫ࡵࠫᡋ"),
  bstack1ll1l1_opy_ (u"ࠫࡵࡸ࡯ࡤࡧࡶࡷࡆࡸࡧࡶ࡯ࡨࡲࡹࡹࠧᡌ"),
  bstack1ll1l1_opy_ (u"ࠬ࡯࡮ࡵࡧࡵࡏࡪࡿࡄࡦ࡮ࡤࡽࠬᡍ"),
  bstack1ll1l1_opy_ (u"࠭ࡳࡩࡱࡺࡍࡔ࡙ࡌࡰࡩࠪᡎ"),
  bstack1ll1l1_opy_ (u"ࠧࡴࡧࡱࡨࡐ࡫ࡹࡔࡶࡵࡥࡹ࡫ࡧࡺࠩᡏ"),
  bstack1ll1l1_opy_ (u"ࠨࡹࡨࡦࡰ࡯ࡴࡓࡧࡶࡴࡴࡴࡳࡦࡖ࡬ࡱࡪࡵࡵࡵࠩᡐ"), bstack1ll1l1_opy_ (u"ࠩࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹ࡝ࡡࡪࡶࡗ࡭ࡲ࡫࡯ࡶࡶࠪᡑ"),
  bstack1ll1l1_opy_ (u"ࠪࡶࡪࡳ࡯ࡵࡧࡇࡩࡧࡻࡧࡑࡴࡲࡼࡾ࠭ᡒ"),
  bstack1ll1l1_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡅࡸࡿ࡮ࡤࡇࡻࡩࡨࡻࡴࡦࡈࡵࡳࡲࡎࡴࡵࡲࡶࠫᡓ"),
  bstack1ll1l1_opy_ (u"ࠬࡹ࡫ࡪࡲࡏࡳ࡬ࡉࡡࡱࡶࡸࡶࡪ࠭ᡔ"),
  bstack1ll1l1_opy_ (u"࠭ࡷࡦࡤ࡮࡭ࡹࡊࡥࡣࡷࡪࡔࡷࡵࡸࡺࡒࡲࡶࡹ࠭ᡕ"),
  bstack1ll1l1_opy_ (u"ࠧࡧࡷ࡯ࡰࡈࡵ࡮ࡵࡧࡻࡸࡑ࡯ࡳࡵࠩᡖ"),
  bstack1ll1l1_opy_ (u"ࠨࡹࡤ࡭ࡹࡌ࡯ࡳࡃࡳࡴࡘࡩࡲࡪࡲࡷࠫᡗ"),
  bstack1ll1l1_opy_ (u"ࠩࡺࡩࡧࡼࡩࡦࡹࡆࡳࡳࡴࡥࡤࡶࡕࡩࡹࡸࡩࡦࡵࠪᡘ"),
  bstack1ll1l1_opy_ (u"ࠪࡥࡵࡶࡎࡢ࡯ࡨࠫᡙ"),
  bstack1ll1l1_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡗࡘࡒࡃࡦࡴࡷࠫᡚ"),
  bstack1ll1l1_opy_ (u"ࠬࡺࡡࡱ࡙࡬ࡸ࡭࡙ࡨࡰࡴࡷࡔࡷ࡫ࡳࡴࡆࡸࡶࡦࡺࡩࡰࡰࠪᡛ"),
  bstack1ll1l1_opy_ (u"࠭ࡳࡤࡣ࡯ࡩࡋࡧࡣࡵࡱࡵࠫᡜ"),
  bstack1ll1l1_opy_ (u"ࠧࡸࡦࡤࡐࡴࡩࡡ࡭ࡒࡲࡶࡹ࠭ᡝ"),
  bstack1ll1l1_opy_ (u"ࠨࡵ࡫ࡳࡼ࡞ࡣࡰࡦࡨࡐࡴ࡭ࠧᡞ"),
  bstack1ll1l1_opy_ (u"ࠩ࡬ࡳࡸࡏ࡮ࡴࡶࡤࡰࡱࡖࡡࡶࡵࡨࠫᡟ"),
  bstack1ll1l1_opy_ (u"ࠪࡼࡨࡵࡤࡦࡅࡲࡲ࡫࡯ࡧࡇ࡫࡯ࡩࠬᡠ"),
  bstack1ll1l1_opy_ (u"ࠫࡰ࡫ࡹࡤࡪࡤ࡭ࡳࡖࡡࡴࡵࡺࡳࡷࡪࠧᡡ"),
  bstack1ll1l1_opy_ (u"ࠬࡻࡳࡦࡒࡵࡩࡧࡻࡩ࡭ࡶ࡚ࡈࡆ࠭ᡢ"),
  bstack1ll1l1_opy_ (u"࠭ࡰࡳࡧࡹࡩࡳࡺࡗࡅࡃࡄࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠧᡣ"),
  bstack1ll1l1_opy_ (u"ࠧࡸࡧࡥࡈࡷ࡯ࡶࡦࡴࡄ࡫ࡪࡴࡴࡖࡴ࡯ࠫᡤ"),
  bstack1ll1l1_opy_ (u"ࠨ࡭ࡨࡽࡨ࡮ࡡࡪࡰࡓࡥࡹ࡮ࠧᡥ"),
  bstack1ll1l1_opy_ (u"ࠩࡸࡷࡪࡔࡥࡸ࡙ࡇࡅࠬᡦ"),
  bstack1ll1l1_opy_ (u"ࠪࡻࡩࡧࡌࡢࡷࡱࡧ࡭࡚ࡩ࡮ࡧࡲࡹࡹ࠭ᡧ"), bstack1ll1l1_opy_ (u"ࠫࡼࡪࡡࡄࡱࡱࡲࡪࡩࡴࡪࡱࡱࡘ࡮ࡳࡥࡰࡷࡷࠫᡨ"),
  bstack1ll1l1_opy_ (u"ࠬࡾࡣࡰࡦࡨࡓࡷ࡭ࡉࡥࠩᡩ"), bstack1ll1l1_opy_ (u"࠭ࡸࡤࡱࡧࡩࡘ࡯ࡧ࡯࡫ࡱ࡫ࡎࡪࠧᡪ"),
  bstack1ll1l1_opy_ (u"ࠧࡶࡲࡧࡥࡹ࡫ࡤࡘࡆࡄࡆࡺࡴࡤ࡭ࡧࡌࡨࠬᡫ"),
  bstack1ll1l1_opy_ (u"ࠨࡴࡨࡷࡪࡺࡏ࡯ࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡷࡺࡏ࡯࡮ࡼࠫᡬ"),
  bstack1ll1l1_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡗ࡭ࡲ࡫࡯ࡶࡶࡶࠫᡭ"),
  bstack1ll1l1_opy_ (u"ࠪࡻࡩࡧࡓࡵࡣࡵࡸࡺࡶࡒࡦࡶࡵ࡭ࡪࡹࠧᡮ"), bstack1ll1l1_opy_ (u"ࠫࡼࡪࡡࡔࡶࡤࡶࡹࡻࡰࡓࡧࡷࡶࡾࡏ࡮ࡵࡧࡵࡺࡦࡲࠧᡯ"),
  bstack1ll1l1_opy_ (u"ࠬࡩ࡯࡯ࡰࡨࡧࡹࡎࡡࡳࡦࡺࡥࡷ࡫ࡋࡦࡻࡥࡳࡦࡸࡤࠨᡰ"),
  bstack1ll1l1_opy_ (u"࠭࡭ࡢࡺࡗࡽࡵ࡯࡮ࡨࡈࡵࡩࡶࡻࡥ࡯ࡥࡼࠫᡱ"),
  bstack1ll1l1_opy_ (u"ࠧࡴ࡫ࡰࡴࡱ࡫ࡉࡴࡘ࡬ࡷ࡮ࡨ࡬ࡦࡅ࡫ࡩࡨࡱࠧᡲ"),
  bstack1ll1l1_opy_ (u"ࠨࡷࡶࡩࡈࡧࡲࡵࡪࡤ࡫ࡪ࡙ࡳ࡭ࠩᡳ"),
  bstack1ll1l1_opy_ (u"ࠩࡶ࡬ࡴࡻ࡬ࡥࡗࡶࡩࡘ࡯࡮ࡨ࡮ࡨࡸࡴࡴࡔࡦࡵࡷࡑࡦࡴࡡࡨࡧࡵࠫᡴ"),
  bstack1ll1l1_opy_ (u"ࠪࡷࡹࡧࡲࡵࡋ࡚ࡈࡕ࠭ᡵ"),
  bstack1ll1l1_opy_ (u"ࠫࡦࡲ࡬ࡰࡹࡗࡳࡺࡩࡨࡊࡦࡈࡲࡷࡵ࡬࡭ࠩᡶ"),
  bstack1ll1l1_opy_ (u"ࠬ࡯ࡧ࡯ࡱࡵࡩࡍ࡯ࡤࡥࡧࡱࡅࡵ࡯ࡐࡰ࡮࡬ࡧࡾࡋࡲࡳࡱࡵࠫᡷ"),
  bstack1ll1l1_opy_ (u"࠭࡭ࡰࡥ࡮ࡐࡴࡩࡡࡵ࡫ࡲࡲࡆࡶࡰࠨᡸ"),
  bstack1ll1l1_opy_ (u"ࠧ࡭ࡱࡪࡧࡦࡺࡆࡰࡴࡰࡥࡹ࠭᡹"), bstack1ll1l1_opy_ (u"ࠨ࡮ࡲ࡫ࡨࡧࡴࡇ࡫࡯ࡸࡪࡸࡓࡱࡧࡦࡷࠬ᡺"),
  bstack1ll1l1_opy_ (u"ࠩࡤࡰࡱࡵࡷࡅࡧ࡯ࡥࡾࡇࡤࡣࠩ᡻"),
  bstack1ll1l1_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨࡍࡩࡒ࡯ࡤࡣࡷࡳࡷࡇࡵࡵࡱࡦࡳࡲࡶ࡬ࡦࡶ࡬ࡳࡳ࠭᡼")
]
bstack11l1lll1l1_opy_ = bstack1ll1l1_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡧࡰࡪ࠯ࡦࡰࡴࡻࡤ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡦࡶࡰ࠮ࡣࡸࡸࡴࡳࡡࡵࡧ࠲ࡹࡵࡲ࡯ࡢࡦࠪ᡽")
bstack1l111ll1ll_opy_ = [bstack1ll1l1_opy_ (u"ࠬ࠴ࡡࡱ࡭ࠪ᡾"), bstack1ll1l1_opy_ (u"࠭࠮ࡢࡣࡥࠫ᡿"), bstack1ll1l1_opy_ (u"ࠧ࠯࡫ࡳࡥࠬᢀ")]
bstack1ll1l1l1l1_opy_ = [bstack1ll1l1_opy_ (u"ࠨ࡫ࡧࠫᢁ"), bstack1ll1l1_opy_ (u"ࠩࡳࡥࡹ࡮ࠧᢂ"), bstack1ll1l1_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡢ࡭ࡩ࠭ᢃ"), bstack1ll1l1_opy_ (u"ࠫࡸ࡮ࡡࡳࡧࡤࡦࡱ࡫࡟ࡪࡦࠪᢄ")]
bstack1lll1l11_opy_ = {
  bstack1ll1l1_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᢅ"): bstack1ll1l1_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᢆ"),
  bstack1ll1l1_opy_ (u"ࠧࡧ࡫ࡵࡩ࡫ࡵࡸࡐࡲࡷ࡭ࡴࡴࡳࠨᢇ"): bstack1ll1l1_opy_ (u"ࠨ࡯ࡲࡾ࠿࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭ᢈ"),
  bstack1ll1l1_opy_ (u"ࠩࡨࡨ࡬࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᢉ"): bstack1ll1l1_opy_ (u"ࠪࡱࡸࡀࡥࡥࡩࡨࡓࡵࡺࡩࡰࡰࡶࠫᢊ"),
  bstack1ll1l1_opy_ (u"ࠫ࡮࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᢋ"): bstack1ll1l1_opy_ (u"ࠬࡹࡥ࠻࡫ࡨࡓࡵࡺࡩࡰࡰࡶࠫᢌ"),
  bstack1ll1l1_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮ࡕࡰࡵ࡫ࡲࡲࡸ࠭ᢍ"): bstack1ll1l1_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯࠮ࡰࡲࡷ࡭ࡴࡴࡳࠨᢎ")
}
bstack11ll11111_opy_ = [
  bstack1ll1l1_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᢏ"),
  bstack1ll1l1_opy_ (u"ࠩࡰࡳࡿࡀࡦࡪࡴࡨࡪࡴࡾࡏࡱࡶ࡬ࡳࡳࡹࠧᢐ"),
  bstack1ll1l1_opy_ (u"ࠪࡱࡸࡀࡥࡥࡩࡨࡓࡵࡺࡩࡰࡰࡶࠫᢑ"),
  bstack1ll1l1_opy_ (u"ࠫࡸ࡫࠺ࡪࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᢒ"),
  bstack1ll1l1_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭࠳ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᢓ"),
]
bstack11111l11l_opy_ = bstack11l1l11ll1_opy_ + bstack11ll1l1ll1l_opy_ + bstack1lll11l11l_opy_
bstack1l1l11l1_opy_ = [
  bstack1ll1l1_opy_ (u"࠭࡞࡭ࡱࡦࡥࡱ࡮࡯ࡴࡶࠧࠫᢔ"),
  bstack1ll1l1_opy_ (u"ࠧ࡟ࡤࡶ࠱ࡱࡵࡣࡢ࡮࠱ࡧࡴࡳࠤࠨᢕ"),
  bstack1ll1l1_opy_ (u"ࠨࡠ࠴࠶࠼࠴ࠧᢖ"),
  bstack1ll1l1_opy_ (u"ࠩࡡ࠵࠵࠴ࠧᢗ"),
  bstack1ll1l1_opy_ (u"ࠪࡢ࠶࠽࠲࠯࠳࡞࠺࠲࠿࡝࠯ࠩᢘ"),
  bstack1ll1l1_opy_ (u"ࠫࡣ࠷࠷࠳࠰࠵࡟࠵࠳࠹࡞࠰ࠪᢙ"),
  bstack1ll1l1_opy_ (u"ࠬࡤ࠱࠸࠴࠱࠷ࡠ࠶࠭࠲࡟࠱ࠫᢚ"),
  bstack1ll1l1_opy_ (u"࠭࡞࠲࠻࠵࠲࠶࠼࠸࠯ࠩᢛ")
]
bstack11ll1l1l1ll_opy_ = bstack1ll1l1_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡣࡳ࡭࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨᢜ")
bstack11llll1ll_opy_ = bstack1ll1l1_opy_ (u"ࠨࡵࡧ࡯࠴ࡼ࠱࠰ࡧࡹࡩࡳࡺࠧᢝ")
bstack1llll11lll_opy_ = [ bstack1ll1l1_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨࠫᢞ") ]
bstack1l1l1111ll_opy_ = [ bstack1ll1l1_opy_ (u"ࠪࡥࡵࡶ࠭ࡢࡷࡷࡳࡲࡧࡴࡦࠩᢟ") ]
bstack1ll11ll11_opy_ = [bstack1ll1l1_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨᢠ")]
bstack1lll1l1l11_opy_ = [ bstack1ll1l1_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬᢡ") ]
bstack11lll111l1_opy_ = bstack1ll1l1_opy_ (u"࠭ࡓࡅࡍࡖࡩࡹࡻࡰࠨᢢ")
bstack1l1lll1l_opy_ = bstack1ll1l1_opy_ (u"ࠧࡔࡆࡎࡘࡪࡹࡴࡂࡶࡷࡩࡲࡶࡴࡦࡦࠪᢣ")
bstack1lllllllll_opy_ = bstack1ll1l1_opy_ (u"ࠨࡕࡇࡏ࡙࡫ࡳࡵࡕࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࠬᢤ")
bstack1111lll11_opy_ = bstack1ll1l1_opy_ (u"ࠩ࠷࠲࠵࠴࠰ࠨᢥ")
bstack1l111l11ll_opy_ = [
  bstack1ll1l1_opy_ (u"ࠪࡉࡗࡘ࡟ࡇࡃࡌࡐࡊࡊࠧᢦ"),
  bstack1ll1l1_opy_ (u"ࠫࡊࡘࡒࡠࡖࡌࡑࡊࡊ࡟ࡐࡗࡗࠫᢧ"),
  bstack1ll1l1_opy_ (u"ࠬࡋࡒࡓࡡࡅࡐࡔࡉࡋࡆࡆࡢࡆ࡞ࡥࡃࡍࡋࡈࡒ࡙࠭ᢨ"),
  bstack1ll1l1_opy_ (u"࠭ࡅࡓࡔࡢࡒࡊ࡚ࡗࡐࡔࡎࡣࡈࡎࡁࡏࡉࡈࡈᢩࠬ"),
  bstack1ll1l1_opy_ (u"ࠧࡆࡔࡕࡣࡘࡕࡃࡌࡇࡗࡣࡓࡕࡔࡠࡅࡒࡒࡓࡋࡃࡕࡇࡇࠫᢪ"),
  bstack1ll1l1_opy_ (u"ࠨࡇࡕࡖࡤࡉࡏࡏࡐࡈࡇ࡙ࡏࡏࡏࡡࡆࡐࡔ࡙ࡅࡅࠩ᢫"),
  bstack1ll1l1_opy_ (u"ࠩࡈࡖࡗࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡖࡊ࡙ࡅࡕࠩ᢬"),
  bstack1ll1l1_opy_ (u"ࠪࡉࡗࡘ࡟ࡄࡑࡑࡒࡊࡉࡔࡊࡑࡑࡣࡗࡋࡆࡖࡕࡈࡈࠬ᢭"),
  bstack1ll1l1_opy_ (u"ࠫࡊࡘࡒࡠࡅࡒࡒࡓࡋࡃࡕࡋࡒࡒࡤࡇࡂࡐࡔࡗࡉࡉ࠭᢮"),
  bstack1ll1l1_opy_ (u"ࠬࡋࡒࡓࡡࡆࡓࡓࡔࡅࡄࡖࡌࡓࡓࡥࡆࡂࡋࡏࡉࡉ࠭᢯"),
  bstack1ll1l1_opy_ (u"࠭ࡅࡓࡔࡢࡒࡆࡓࡅࡠࡐࡒࡘࡤࡘࡅࡔࡑࡏ࡚ࡊࡊࠧᢰ"),
  bstack1ll1l1_opy_ (u"ࠧࡆࡔࡕࡣࡆࡊࡄࡓࡇࡖࡗࡤࡏࡎࡗࡃࡏࡍࡉ࠭ᢱ"),
  bstack1ll1l1_opy_ (u"ࠨࡇࡕࡖࡤࡇࡄࡅࡔࡈࡗࡘࡥࡕࡏࡔࡈࡅࡈࡎࡁࡃࡎࡈࠫᢲ"),
  bstack1ll1l1_opy_ (u"ࠩࡈࡖࡗࡥࡔࡖࡐࡑࡉࡑࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡊࡆࡏࡌࡆࡆࠪᢳ"),
  bstack1ll1l1_opy_ (u"ࠪࡉࡗࡘ࡟ࡄࡑࡑࡒࡊࡉࡔࡊࡑࡑࡣ࡙ࡏࡍࡆࡆࡢࡓ࡚࡚ࠧᢴ"),
  bstack1ll1l1_opy_ (u"ࠫࡊࡘࡒࡠࡕࡒࡇࡐ࡙࡟ࡄࡑࡑࡒࡊࡉࡔࡊࡑࡑࡣࡋࡇࡉࡍࡇࡇࠫᢵ"),
  bstack1ll1l1_opy_ (u"ࠬࡋࡒࡓࡡࡖࡓࡈࡑࡓࡠࡅࡒࡒࡓࡋࡃࡕࡋࡒࡒࡤࡎࡏࡔࡖࡢ࡙ࡓࡘࡅࡂࡅࡋࡅࡇࡒࡅࠨᢶ"),
  bstack1ll1l1_opy_ (u"࠭ࡅࡓࡔࡢࡔࡗࡕࡘ࡚ࡡࡆࡓࡓࡔࡅࡄࡖࡌࡓࡓࡥࡆࡂࡋࡏࡉࡉ࠭ᢷ"),
  bstack1ll1l1_opy_ (u"ࠧࡆࡔࡕࡣࡓࡇࡍࡆࡡࡑࡓ࡙ࡥࡒࡆࡕࡒࡐ࡛ࡋࡄࠨᢸ"),
  bstack1ll1l1_opy_ (u"ࠨࡇࡕࡖࡤࡔࡁࡎࡇࡢࡖࡊ࡙ࡏࡍࡗࡗࡍࡔࡔ࡟ࡇࡃࡌࡐࡊࡊࠧᢹ"),
  bstack1ll1l1_opy_ (u"ࠩࡈࡖࡗࡥࡍࡂࡐࡇࡅ࡙ࡕࡒ࡚ࡡࡓࡖࡔ࡞࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠࡈࡄࡍࡑࡋࡄࠨᢺ"),
]
bstack1l111l111l_opy_ = bstack1ll1l1_opy_ (u"ࠪ࠲࠴ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠱ࡦࡸࡴࡪࡨࡤࡧࡹࡹ࠯ࠨᢻ")
bstack1l111111l1_opy_ = os.path.join(os.path.expanduser(bstack1ll1l1_opy_ (u"ࠫࢃ࠭ᢼ")), bstack1ll1l1_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬᢽ"), bstack1ll1l1_opy_ (u"࠭࠮ࡣࡵࡷࡥࡨࡱ࠭ࡤࡱࡱࡪ࡮࡭࠮࡫ࡵࡲࡲࠬᢾ"))
bstack11lllll1lll_opy_ = bstack1ll1l1_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡦࡶࡩࠨᢿ")
bstack11ll1l11ll1_opy_ = [ bstack1ll1l1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨᣀ"), bstack1ll1l1_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨᣁ"), bstack1ll1l1_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩᣂ"), bstack1ll1l1_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫᣃ")]
bstack1l1ll11l1_opy_ = [ bstack1ll1l1_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬᣄ"), bstack1ll1l1_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬᣅ"), bstack1ll1l1_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭ᣆ"), bstack1ll1l1_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨᣇ") ]
bstack11ll1l1111_opy_ = [ bstack1ll1l1_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨᣈ") ]
bstack1l1111l11l_opy_ = 360
bstack11lll1l1lll_opy_ = bstack1ll1l1_opy_ (u"ࠥࡥࡵࡶ࠭ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠥᣉ")
bstack11ll1l111l1_opy_ = bstack1ll1l1_opy_ (u"ࠦࡦࡻࡴࡰ࡯ࡤࡸࡪ࠵ࡡࡱ࡫࠲ࡺ࠶࠵ࡩࡴࡵࡸࡩࡸࠨᣊ")
bstack11ll1l1111l_opy_ = bstack1ll1l1_opy_ (u"ࠧࡧࡵࡵࡱࡰࡥࡹ࡫࠯ࡢࡲ࡬࠳ࡻ࠷࠯ࡪࡵࡶࡹࡪࡹ࠭ࡴࡷࡰࡱࡦࡸࡹࠣᣋ")
bstack11lllll1l11_opy_ = bstack1ll1l1_opy_ (u"ࠨࡁࡱࡲࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡵࡧࡶࡸࡸࠦࡡࡳࡧࠣࡷࡺࡶࡰࡰࡴࡷࡩࡩࠦ࡯࡯ࠢࡒࡗࠥࡼࡥࡳࡵ࡬ࡳࡳࠦࠥࡴࠢࡤࡲࡩࠦࡡࡣࡱࡹࡩࠥ࡬࡯ࡳࠢࡄࡲࡩࡸ࡯ࡪࡦࠣࡨࡪࡼࡩࡤࡧࡶ࠲ࠧᣌ")
bstack11lllll11ll_opy_ = bstack1ll1l1_opy_ (u"ࠢ࠲࠳࠱࠴ࠧᣍ")
bstack111l1ll1ll_opy_ = {
  bstack1ll1l1_opy_ (u"ࠨࡒࡄࡗࡘ࠭ᣎ"): bstack1ll1l1_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩᣏ"),
  bstack1ll1l1_opy_ (u"ࠪࡊࡆࡏࡌࠨᣐ"): bstack1ll1l1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᣑ"),
  bstack1ll1l1_opy_ (u"࡙ࠬࡋࡊࡒࠪᣒ"): bstack1ll1l1_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧᣓ")
}
bstack1l1lll11ll_opy_ = [
  bstack1ll1l1_opy_ (u"ࠢࡨࡧࡷࠦᣔ"),
  bstack1ll1l1_opy_ (u"ࠣࡩࡲࡆࡦࡩ࡫ࠣᣕ"),
  bstack1ll1l1_opy_ (u"ࠤࡪࡳࡋࡵࡲࡸࡣࡵࡨࠧᣖ"),
  bstack1ll1l1_opy_ (u"ࠥࡶࡪ࡬ࡲࡦࡵ࡫ࠦᣗ"),
  bstack1ll1l1_opy_ (u"ࠦࡨࡲࡩࡤ࡭ࡈࡰࡪࡳࡥ࡯ࡶࠥᣘ"),
  bstack1ll1l1_opy_ (u"ࠧࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠤᣙ"),
  bstack1ll1l1_opy_ (u"ࠨࡳࡶࡤࡰ࡭ࡹࡋ࡬ࡦ࡯ࡨࡲࡹࠨᣚ"),
  bstack1ll1l1_opy_ (u"ࠢࡴࡧࡱࡨࡐ࡫ࡹࡴࡖࡲࡉࡱ࡫࡭ࡦࡰࡷࠦᣛ"),
  bstack1ll1l1_opy_ (u"ࠣࡵࡨࡲࡩࡑࡥࡺࡵࡗࡳࡆࡩࡴࡪࡸࡨࡉࡱ࡫࡭ࡦࡰࡷࠦᣜ"),
  bstack1ll1l1_opy_ (u"ࠤࡦࡰࡪࡧࡲࡆ࡮ࡨࡱࡪࡴࡴࠣᣝ"),
  bstack1ll1l1_opy_ (u"ࠥࡥࡨࡺࡩࡰࡰࡶࠦᣞ"),
  bstack1ll1l1_opy_ (u"ࠦࡪࡾࡥࡤࡷࡷࡩࡘࡩࡲࡪࡲࡷࠦᣟ"),
  bstack1ll1l1_opy_ (u"ࠧ࡫ࡸࡦࡥࡸࡸࡪࡇࡳࡺࡰࡦࡗࡨࡸࡩࡱࡶࠥᣠ"),
  bstack1ll1l1_opy_ (u"ࠨࡣ࡭ࡱࡶࡩࠧᣡ"),
  bstack1ll1l1_opy_ (u"ࠢࡲࡷ࡬ࡸࠧᣢ"),
  bstack1ll1l1_opy_ (u"ࠣࡲࡨࡶ࡫ࡵࡲ࡮ࡖࡲࡹࡨ࡮ࡁࡤࡶ࡬ࡳࡳࠨᣣ"),
  bstack1ll1l1_opy_ (u"ࠤࡳࡩࡷ࡬࡯ࡳ࡯ࡐࡹࡱࡺࡩࡕࡱࡸࡧ࡭ࠨᣤ"),
  bstack1ll1l1_opy_ (u"ࠥࡷ࡭ࡧ࡫ࡦࠤᣥ"),
  bstack1ll1l1_opy_ (u"ࠦࡨࡲ࡯ࡴࡧࡄࡴࡵࠨᣦ")
]
bstack11lll1111l1_opy_ = [
  bstack1ll1l1_opy_ (u"ࠧࡩ࡬ࡪࡥ࡮ࠦᣧ"),
  bstack1ll1l1_opy_ (u"ࠨࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠥᣨ"),
  bstack1ll1l1_opy_ (u"ࠢࡢࡷࡷࡳࠧᣩ"),
  bstack1ll1l1_opy_ (u"ࠣ࡯ࡤࡲࡺࡧ࡬ࠣᣪ"),
  bstack1ll1l1_opy_ (u"ࠤࡷࡩࡸࡺࡣࡢࡵࡨࠦᣫ")
]
bstack11111ll1l_opy_ = {
  bstack1ll1l1_opy_ (u"ࠥࡧࡱ࡯ࡣ࡬ࠤᣬ"): [bstack1ll1l1_opy_ (u"ࠦࡨࡲࡩࡤ࡭ࡈࡰࡪࡳࡥ࡯ࡶࠥᣭ")],
  bstack1ll1l1_opy_ (u"ࠧࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠤᣮ"): [bstack1ll1l1_opy_ (u"ࠨࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠥᣯ")],
  bstack1ll1l1_opy_ (u"ࠢࡢࡷࡷࡳࠧᣰ"): [bstack1ll1l1_opy_ (u"ࠣࡵࡨࡲࡩࡑࡥࡺࡵࡗࡳࡊࡲࡥ࡮ࡧࡱࡸࠧᣱ"), bstack1ll1l1_opy_ (u"ࠤࡶࡩࡳࡪࡋࡦࡻࡶࡘࡴࡇࡣࡵ࡫ࡹࡩࡊࡲࡥ࡮ࡧࡱࡸࠧᣲ"), bstack1ll1l1_opy_ (u"ࠥࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠢᣳ"), bstack1ll1l1_opy_ (u"ࠦࡨࡲࡩࡤ࡭ࡈࡰࡪࡳࡥ࡯ࡶࠥᣴ")],
  bstack1ll1l1_opy_ (u"ࠧࡳࡡ࡯ࡷࡤࡰࠧᣵ"): [bstack1ll1l1_opy_ (u"ࠨ࡭ࡢࡰࡸࡥࡱࠨ᣶")],
  bstack1ll1l1_opy_ (u"ࠢࡵࡧࡶࡸࡨࡧࡳࡦࠤ᣷"): [bstack1ll1l1_opy_ (u"ࠣࡶࡨࡷࡹࡩࡡࡴࡧࠥ᣸")],
}
bstack11ll1l1llll_opy_ = {
  bstack1ll1l1_opy_ (u"ࠤࡦࡰ࡮ࡩ࡫ࡆ࡮ࡨࡱࡪࡴࡴࠣ᣹"): bstack1ll1l1_opy_ (u"ࠥࡧࡱ࡯ࡣ࡬ࠤ᣺"),
  bstack1ll1l1_opy_ (u"ࠦࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠣ᣻"): bstack1ll1l1_opy_ (u"ࠧࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠤ᣼"),
  bstack1ll1l1_opy_ (u"ࠨࡳࡦࡰࡧࡏࡪࡿࡳࡕࡱࡈࡰࡪࡳࡥ࡯ࡶࠥ᣽"): bstack1ll1l1_opy_ (u"ࠢࡴࡧࡱࡨࡐ࡫ࡹࡴࠤ᣾"),
  bstack1ll1l1_opy_ (u"ࠣࡵࡨࡲࡩࡑࡥࡺࡵࡗࡳࡆࡩࡴࡪࡸࡨࡉࡱ࡫࡭ࡦࡰࡷࠦ᣿"): bstack1ll1l1_opy_ (u"ࠤࡶࡩࡳࡪࡋࡦࡻࡶࠦᤀ"),
  bstack1ll1l1_opy_ (u"ࠥࡸࡪࡹࡴࡤࡣࡶࡩࠧᤁ"): bstack1ll1l1_opy_ (u"ࠦࡹ࡫ࡳࡵࡥࡤࡷࡪࠨᤂ")
}
bstack111llll111_opy_ = {
  bstack1ll1l1_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡇࡌࡍࠩᤃ"): bstack1ll1l1_opy_ (u"࠭ࡓࡶ࡫ࡷࡩ࡙ࠥࡥࡵࡷࡳࠫᤄ"),
  bstack1ll1l1_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡁࡍࡎࠪᤅ"): bstack1ll1l1_opy_ (u"ࠨࡕࡸ࡭ࡹ࡫ࠠࡕࡧࡤࡶࡩࡵࡷ࡯ࠩᤆ"),
  bstack1ll1l1_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧᤇ"): bstack1ll1l1_opy_ (u"ࠪࡘࡪࡹࡴࠡࡕࡨࡸࡺࡶࠧᤈ"),
  bstack1ll1l1_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡉࡆࡉࡈࠨᤉ"): bstack1ll1l1_opy_ (u"࡚ࠬࡥࡴࡶࠣࡘࡪࡧࡲࡥࡱࡺࡲࠬᤊ")
}
bstack11ll1llll11_opy_ = 65536
bstack11ll1ll1l1l_opy_ = bstack1ll1l1_opy_ (u"࠭࠮࠯࠰࡞ࡘࡗ࡛ࡎࡄࡃࡗࡉࡉࡣࠧᤋ")
bstack11ll1ll1ll1_opy_ = [
      bstack1ll1l1_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩᤌ"), bstack1ll1l1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫᤍ"), bstack1ll1l1_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬᤎ"), bstack1ll1l1_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧᤏ"), bstack1ll1l1_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰ࡚ࡦࡸࡩࡢࡤ࡯ࡩࡸ࠭ᤐ"),
      bstack1ll1l1_opy_ (u"ࠬࡶࡲࡰࡺࡼ࡙ࡸ࡫ࡲࠨᤑ"), bstack1ll1l1_opy_ (u"࠭ࡰࡳࡱࡻࡽࡕࡧࡳࡴࠩᤒ"), bstack1ll1l1_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡖࡲࡰࡺࡼ࡙ࡸ࡫ࡲࠨᤓ"), bstack1ll1l1_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡐࡳࡱࡻࡽࡕࡧࡳࡴࠩᤔ"),
      bstack1ll1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡷࡶࡩࡷࡔࡡ࡮ࡧࠪᤕ"), bstack1ll1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬᤖ"), bstack1ll1l1_opy_ (u"ࠫࡦࡻࡴࡩࡖࡲ࡯ࡪࡴࠧᤗ")
    ]
bstack11ll1lll1ll_opy_= {
  bstack1ll1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩᤘ"): bstack1ll1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪᤙ"),
  bstack1ll1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫᤚ"): bstack1ll1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬᤛ"),
  bstack1ll1l1_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨᤜ"): bstack1ll1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧᤝ"),
  bstack1ll1l1_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫᤞ"): bstack1ll1l1_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ᤟"),
  bstack1ll1l1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩᤠ"): bstack1ll1l1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᤡ"),
  bstack1ll1l1_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪᤢ"): bstack1ll1l1_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫᤣ"),
  bstack1ll1l1_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭ᤤ"): bstack1ll1l1_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧᤥ"),
  bstack1ll1l1_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩᤦ"): bstack1ll1l1_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪᤧ"),
  bstack1ll1l1_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪᤨ"): bstack1ll1l1_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫᤩ"),
  bstack1ll1l1_opy_ (u"ࠩࡷࡩࡸࡺࡃࡰࡰࡷࡩࡽࡺࡏࡱࡶ࡬ࡳࡳࡹࠧᤪ"): bstack1ll1l1_opy_ (u"ࠪࡸࡪࡹࡴࡄࡱࡱࡸࡪࡾࡴࡐࡲࡷ࡭ࡴࡴࡳࠨᤫ"),
  bstack1ll1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨ᤬"): bstack1ll1l1_opy_ (u"ࠬࡺࡥࡴࡶࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ᤭"),
  bstack1ll1l1_opy_ (u"࠭ࡴࡦࡵࡷࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪ᤮"): bstack1ll1l1_opy_ (u"ࠧࡵࡧࡶࡸࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫ᤯"),
  bstack1ll1l1_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡗࡣࡵ࡭ࡦࡨ࡬ࡦࡵࠪᤰ"): bstack1ll1l1_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡘࡤࡶ࡮ࡧࡢ࡭ࡧࡶࠫᤱ"),
  bstack1ll1l1_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᤲ"): bstack1ll1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ᤳ"),
  bstack1ll1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᤴ"): bstack1ll1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨᤵ"),
  bstack1ll1l1_opy_ (u"ࠧࡳࡧࡵࡹࡳ࡚ࡥࡴࡶࡶࠫᤶ"): bstack1ll1l1_opy_ (u"ࠨࡴࡨࡶࡺࡴࡔࡦࡵࡷࡷࠬᤷ"),
  bstack1ll1l1_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨᤸ"): bstack1ll1l1_opy_ (u"ࠪࡴࡪࡸࡣࡺ᤹ࠩ"),
  bstack1ll1l1_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡒࡴࡹ࡯࡯࡯ࡵࠪ᤺"): bstack1ll1l1_opy_ (u"ࠬࡶࡥࡳࡥࡼࡓࡵࡺࡩࡰࡰࡶ᤻ࠫ"),
  bstack1ll1l1_opy_ (u"࠭ࡰࡦࡴࡦࡽࡈࡧࡰࡵࡷࡵࡩࡒࡵࡤࡦࠩ᤼"): bstack1ll1l1_opy_ (u"ࠧࡱࡧࡵࡧࡾࡉࡡࡱࡶࡸࡶࡪࡓ࡯ࡥࡧࠪ᤽"),
  bstack1ll1l1_opy_ (u"ࠨࡦ࡬ࡷࡦࡨ࡬ࡦࡃࡸࡸࡴࡉࡡࡱࡶࡸࡶࡪࡒ࡯ࡨࡵࠪ᤾"): bstack1ll1l1_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡄࡹࡹࡵࡃࡢࡲࡷࡹࡷ࡫ࡌࡰࡩࡶࠫ᤿"),
  bstack1ll1l1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ᥀"): bstack1ll1l1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ᥁"),
  bstack1ll1l1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬ᥂"): bstack1ll1l1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭᥃"),
  bstack1ll1l1_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫ᥄"): bstack1ll1l1_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬ᥅"),
  bstack1ll1l1_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭᥆"): bstack1ll1l1_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ᥇"),
  bstack1ll1l1_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡖࡩࡹࡺࡩ࡯ࡩࡶࠫ᥈"): bstack1ll1l1_opy_ (u"ࠬࡶࡲࡰࡺࡼࡗࡪࡺࡴࡪࡰࡪࡷࠬ᥉")
}
bstack11ll1lll1l1_opy_ = [bstack1ll1l1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭᥊"), bstack1ll1l1_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭᥋")]
bstack111l11111_opy_ = (bstack1ll1l1_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴࠣ᥌"),)
bstack11lll11111l_opy_ = bstack1ll1l1_opy_ (u"ࠩࡶࡨࡰ࠵ࡶ࠲࠱ࡸࡴࡩࡧࡴࡦࡡࡦࡰ࡮࠭᥍")
bstack1l11111ll1_opy_ = bstack1ll1l1_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡦࡶࡩ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠳ࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧ࠲ࡺ࠶࠵ࡧࡳ࡫ࡧࡷ࠴ࠨ᥎")
bstack1lll1llll_opy_ = bstack1ll1l1_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴࡭ࡲࡪࡦ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡤࡢࡵ࡫ࡦࡴࡧࡲࡥ࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࠥ᥏")
bstack11lllll1l1_opy_ = bstack1ll1l1_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡡࡱ࡫࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡡࡶࡶࡲࡱࡦࡺࡥ࠮ࡶࡸࡶࡧࡵࡳࡤࡣ࡯ࡩ࠴ࡼ࠱࠰ࡤࡸ࡭ࡱࡪࡳ࠯࡬ࡶࡳࡳࠨᥐ")
class EVENTS(Enum):
  bstack11ll1l1ll11_opy_ = bstack1ll1l1_opy_ (u"࠭ࡳࡥ࡭࠽ࡳ࠶࠷ࡹ࠻ࡲࡵ࡭ࡳࡺ࠭ࡣࡷ࡬ࡰࡩࡲࡩ࡯࡭ࠪᥑ")
  bstack1llll11111_opy_ = bstack1ll1l1_opy_ (u"ࠧࡴࡦ࡮࠾ࡨࡲࡥࡢࡰࡸࡴࠬᥒ") # final bstack11ll1llllll_opy_
  bstack11ll1l11lll_opy_ = bstack1ll1l1_opy_ (u"ࠨࡵࡧ࡯࠿ࡹࡥ࡯ࡦ࡯ࡳ࡬ࡹࠧᥓ")
  bstack1ll1l1llll_opy_ = bstack1ll1l1_opy_ (u"ࠩࡶࡨࡰࡀࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧ࠽ࡴࡷ࡯࡮ࡵ࠯ࡥࡹ࡮ࡲࡤ࡭࡫ࡱ࡯ࠬᥔ") #shift post bstack11ll1l1lll1_opy_
  bstack1lllll11l_opy_ = bstack1ll1l1_opy_ (u"ࠪࡷࡩࡱ࠺ࡢࡷࡷࡳࡲࡧࡴࡦ࠼ࡳࡶ࡮ࡴࡴ࠮ࡤࡸ࡭ࡱࡪ࡬ࡪࡰ࡮ࠫᥕ") #shift post bstack11ll1l1lll1_opy_
  bstack11ll1l111ll_opy_ = bstack1ll1l1_opy_ (u"ࠫࡸࡪ࡫࠻ࡶࡨࡷࡹ࡮ࡵࡣࠩᥖ") #shift
  bstack11ll1ll1111_opy_ = bstack1ll1l1_opy_ (u"ࠬࡹࡤ࡬࠼ࡳࡩࡷࡩࡹ࠻ࡦࡲࡻࡳࡲ࡯ࡢࡦࠪᥗ") #shift
  bstack1lll1111_opy_ = bstack1ll1l1_opy_ (u"࠭ࡳࡥ࡭࠽ࡸࡺࡸࡢࡰࡵࡦࡥࡱ࡫࠺ࡩࡷࡥ࠱ࡲࡧ࡮ࡢࡩࡨࡱࡪࡴࡴࠨᥘ")
  bstack1ll1l1ll1l1_opy_ = bstack1ll1l1_opy_ (u"ࠧࡴࡦ࡮࠾ࡦ࠷࠱ࡺ࠼ࡶࡥࡻ࡫࠭ࡳࡧࡶࡹࡱࡺࡳࠨᥙ")
  bstack1l11l11ll1_opy_ = bstack1ll1l1_opy_ (u"ࠨࡵࡧ࡯࠿ࡧ࠱࠲ࡻ࠽ࡨࡷ࡯ࡶࡦࡴ࠰ࡴࡪࡸࡦࡰࡴࡰࡷࡨࡧ࡮ࠨᥚ")
  bstack1ll1l1ll_opy_ = bstack1ll1l1_opy_ (u"ࠩࡶࡨࡰࡀࡡࡶࡶࡲࡱࡦࡺࡥ࠻࡮ࡲࡧࡦࡲࠧᥛ") #shift
  bstack1ll11l11_opy_ = bstack1ll1l1_opy_ (u"ࠪࡷࡩࡱ࠺ࡢࡲࡳ࠱ࡦࡻࡴࡰ࡯ࡤࡸࡪࡀࡡࡱࡲ࠰ࡹࡵࡲ࡯ࡢࡦࠪᥜ") #shift
  bstack1ll1l1ll1_opy_ = bstack1ll1l1_opy_ (u"ࠫࡸࡪ࡫࠻ࡣࡸࡸࡴࡳࡡࡵࡧ࠽ࡧ࡮࠳ࡡࡳࡶ࡬ࡪࡦࡩࡴࡴࠩᥝ")
  bstack1l1l11l1l1_opy_ = bstack1ll1l1_opy_ (u"ࠬࡹࡤ࡬࠼ࡤ࠵࠶ࡿ࠺ࡨࡧࡷ࠱ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼ࠱ࡷ࡫ࡳࡶ࡮ࡷࡷ࠲ࡹࡵ࡮࡯ࡤࡶࡾ࠭ᥞ") #shift
  bstack1111l1lll_opy_ = bstack1ll1l1_opy_ (u"࠭ࡳࡥ࡭࠽ࡥ࠶࠷ࡹ࠻ࡩࡨࡸ࠲ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽ࠲ࡸࡥࡴࡷ࡯ࡸࡸ࠭ᥟ") #shift
  bstack11ll1lll11l_opy_ = bstack1ll1l1_opy_ (u"ࠧࡴࡦ࡮࠾ࡵ࡫ࡲࡤࡻࠪᥠ") #shift
  bstack1l1ll1ll111_opy_ = bstack1ll1l1_opy_ (u"ࠨࡵࡧ࡯࠿ࡶࡥࡳࡥࡼ࠾ࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠨᥡ")
  bstack1l1ll11l11_opy_ = bstack1ll1l1_opy_ (u"ࠩࡶࡨࡰࡀࡡࡶࡶࡲࡱࡦࡺࡥ࠻ࡵࡨࡷࡸ࡯࡯࡯࠯ࡶࡸࡦࡺࡵࡴࠩᥢ") #shift
  bstack11l11ll1_opy_ = bstack1ll1l1_opy_ (u"ࠪࡷࡩࡱ࠺ࡢࡷࡷࡳࡲࡧࡴࡦ࠼࡫ࡹࡧ࠳࡭ࡢࡰࡤ࡫ࡪࡳࡥ࡯ࡶࠪᥣ")
  bstack11ll1l11l1l_opy_ = bstack1ll1l1_opy_ (u"ࠫࡸࡪ࡫࠻ࡲࡵࡳࡽࡿ࠭ࡴࡧࡷࡹࡵ࠭ᥤ") #shift
  bstack1ll1lll1_opy_ = bstack1ll1l1_opy_ (u"ࠬࡹࡤ࡬࠼ࡶࡩࡹࡻࡰࠨᥥ")
  bstack11ll1llll1l_opy_ = bstack1ll1l1_opy_ (u"࠭ࡳࡥ࡭࠽ࡴࡪࡸࡣࡺ࠼ࡶࡲࡦࡶࡳࡩࡱࡷࠫᥦ") # not bstack11lll111l11_opy_ in python
  bstack1ll1ll111_opy_ = bstack1ll1l1_opy_ (u"ࠧࡴࡦ࡮࠾ࡩࡸࡩࡷࡧࡵ࠾ࡶࡻࡩࡵࠩᥧ") # used in bstack11ll1l1l11l_opy_
  bstack1ll11ll1_opy_ = bstack1ll1l1_opy_ (u"ࠨࡵࡧ࡯࠿ࡪࡲࡪࡸࡨࡶ࠿࡭ࡥࡵࠩᥨ") # used in bstack11ll1l1l11l_opy_
  bstack1l1ll1ll_opy_ = bstack1ll1l1_opy_ (u"ࠩࡶࡨࡰࡀࡨࡰࡱ࡮ࠫᥩ")
  bstack11l1l11ll_opy_ = bstack1ll1l1_opy_ (u"ࠪࡷࡩࡱ࠺ࡢࡷࡷࡳࡲࡧࡴࡦ࠼ࡶࡩࡸࡹࡩࡰࡰ࠰ࡲࡦࡳࡥࠨᥪ")
  bstack11lllllll1_opy_ = bstack1ll1l1_opy_ (u"ࠫࡸࡪ࡫࠻ࡣࡸࡸࡴࡳࡡࡵࡧ࠽ࡷࡪࡹࡳࡪࡱࡱ࠱ࡦࡴ࡮ࡰࡶࡤࡸ࡮ࡵ࡮ࠨᥫ") #
  bstack111lll11_opy_ = bstack1ll1l1_opy_ (u"ࠬࡹࡤ࡬࠼ࡲ࠵࠶ࡿ࠺ࡥࡴ࡬ࡺࡪࡸ࠭ࡵࡣ࡮ࡩࡘࡩࡲࡦࡧࡱࡗ࡭ࡵࡴࠨᥬ")
  bstack1llll1l11_opy_ = bstack1ll1l1_opy_ (u"࠭ࡳࡥ࡭࠽ࡴࡪࡸࡣࡺ࠼ࡤࡹࡹࡵ࠭ࡤࡣࡳࡸࡺࡸࡥࠨᥭ")
  bstack1l1ll1l111_opy_ = bstack1ll1l1_opy_ (u"ࠧࡴࡦ࡮࠾ࡵࡸࡥ࠮ࡶࡨࡷࡹ࠭᥮")
  bstack11l1ll1l1_opy_ = bstack1ll1l1_opy_ (u"ࠨࡵࡧ࡯࠿ࡶ࡯ࡴࡶ࠰ࡸࡪࡹࡴࠨ᥯")
  bstack1l11lll11l_opy_ = bstack1ll1l1_opy_ (u"ࠩࡶࡨࡰࡀࡤࡳ࡫ࡹࡩࡷࡀࡰࡳࡧ࠰࡭ࡳ࡯ࡴࡪࡣ࡯࡭ࡿࡧࡴࡪࡱࡱࠫᥰ") #shift
  bstack1l1l1lllll_opy_ = bstack1ll1l1_opy_ (u"ࠪࡷࡩࡱ࠺ࡥࡴ࡬ࡺࡪࡸ࠺ࡱࡱࡶࡸ࠲࡯࡮ࡪࡶ࡬ࡥࡱ࡯ࡺࡢࡶ࡬ࡳࡳ࠭ᥱ") #shift
  bstack11ll1ll111l_opy_ = bstack1ll1l1_opy_ (u"ࠫࡸࡪ࡫࠻ࡣࡸࡸࡴ࠳ࡣࡢࡲࡷࡹࡷ࡫ࠧᥲ")
  bstack11lll111l1l_opy_ = bstack1ll1l1_opy_ (u"ࠬࡹࡤ࡬࠼ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠾࡮ࡪ࡬ࡦ࠯ࡷ࡭ࡲ࡫࡯ࡶࡶࠪᥳ")
  bstack1llll11l1ll_opy_ = bstack1ll1l1_opy_ (u"࠭ࡳࡥ࡭࠽ࡧࡱ࡯࠺ࡴࡶࡤࡶࡹ࠭ᥴ")
  bstack11ll1l1l111_opy_ = bstack1ll1l1_opy_ (u"ࠧࡴࡦ࡮࠾ࡨࡲࡩ࠻ࡦࡲࡻࡳࡲ࡯ࡢࡦࠪ᥵")
  bstack11ll1ll1lll_opy_ = bstack1ll1l1_opy_ (u"ࠨࡵࡧ࡯࠿ࡩ࡬ࡪ࠼ࡦ࡬ࡪࡩ࡫࠮ࡷࡳࡨࡦࡺࡥࠨ᥶")
  bstack1lll1l1lll1_opy_ = bstack1ll1l1_opy_ (u"ࠩࡶࡨࡰࡀࡣ࡭࡫࠽ࡳࡳ࠳ࡢࡰࡱࡷࡷࡹࡸࡡࡱࠩ᥷")
  bstack1lll11lll1l_opy_ = bstack1ll1l1_opy_ (u"ࠪࡷࡩࡱ࠺ࡤ࡮࡬࠾ࡴࡴ࠭ࡤࡱࡱࡲࡪࡩࡴࠨ᥸")
  bstack1lll1l111ll_opy_ = bstack1ll1l1_opy_ (u"ࠫࡸࡪ࡫࠻ࡥ࡯࡭࠿ࡵ࡮࠮ࡵࡷࡳࡵ࠭᥹")
  bstack1llllll11ll_opy_ = bstack1ll1l1_opy_ (u"ࠬࡹࡤ࡬࠼ࡶࡸࡦࡸࡴࡃ࡫ࡱࡗࡪࡹࡳࡪࡱࡱࠫ᥺")
  bstack1llll1l1l1l_opy_ = bstack1ll1l1_opy_ (u"࠭ࡳࡥ࡭࠽ࡧࡴࡴ࡮ࡦࡥࡷࡆ࡮ࡴࡓࡦࡵࡶ࡭ࡴࡴࠧ᥻")
  bstack11ll1lll111_opy_ = bstack1ll1l1_opy_ (u"ࠧࡴࡦ࡮࠾ࡩࡸࡩࡷࡧࡵࡍࡳ࡯ࡴࠨ᥼")
  bstack11ll1lllll1_opy_ = bstack1ll1l1_opy_ (u"ࠨࡵࡧ࡯࠿࡬ࡩ࡯ࡦࡑࡩࡦࡸࡥࡴࡶࡋࡹࡧ࠭᥽")
  bstack1l1l1l11ll1_opy_ = bstack1ll1l1_opy_ (u"ࠩࡶࡨࡰࡀࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࡎࡴࡩࡵࠩ᥾")
  bstack1l1l11l1lll_opy_ = bstack1ll1l1_opy_ (u"ࠪࡷࡩࡱ࠺ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࡙ࡴࡢࡴࡷࠫ᥿")
  bstack1ll1l11llll_opy_ = bstack1ll1l1_opy_ (u"ࠫࡸࡪ࡫࠻ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡄࡱࡱࡪ࡮࡭ࠧᦀ")
  bstack11ll1ll11ll_opy_ = bstack1ll1l1_opy_ (u"ࠬࡹࡤ࡬࠼ࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࡅࡲࡲ࡫࡯ࡧࠨᦁ")
  bstack1ll11lll1l1_opy_ = bstack1ll1l1_opy_ (u"࠭ࡳࡥ࡭࠽ࡥ࡮࡙ࡥ࡭ࡨࡋࡩࡦࡲࡓࡵࡧࡳࠫᦂ")
  bstack1ll11llll11_opy_ = bstack1ll1l1_opy_ (u"ࠧࡴࡦ࡮࠾ࡦ࡯ࡓࡦ࡮ࡩࡌࡪࡧ࡬ࡈࡧࡷࡖࡪࡹࡵ࡭ࡶࠪᦃ")
  bstack1l1lll1l1ll_opy_ = bstack1ll1l1_opy_ (u"ࠨࡵࡧ࡯࠿ࡺࡥࡴࡶࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࡊࡼࡥ࡯ࡶࠪᦄ")
  bstack1l1lllllll1_opy_ = bstack1ll1l1_opy_ (u"ࠩࡶࡨࡰࡀࡴࡦࡵࡷࡗࡪࡹࡳࡪࡱࡱࡉࡻ࡫࡮ࡵࠩᦅ")
  bstack1ll11111l11_opy_ = bstack1ll1l1_opy_ (u"ࠪࡷࡩࡱ࠺ࡤ࡮࡬࠾ࡱࡵࡧࡄࡴࡨࡥࡹ࡫ࡤࡆࡸࡨࡲࡹ࠭ᦆ")
  bstack11ll1ll11l1_opy_ = bstack1ll1l1_opy_ (u"ࠫࡸࡪ࡫࠻ࡥ࡯࡭࠿࡫࡮ࡲࡷࡨࡹࡪ࡚ࡥࡴࡶࡈࡺࡪࡴࡴࠨᦇ")
  bstack1l1l11ll1l1_opy_ = bstack1ll1l1_opy_ (u"ࠬࡹࡤ࡬࠼ࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡔࡶࡲࡴࠬᦈ")
  bstack1llll1ll1l1_opy_ = bstack1ll1l1_opy_ (u"࠭ࡳࡥ࡭࠽ࡳࡳ࡙ࡴࡰࡲࠪᦉ")
class STAGE(Enum):
  bstack1l11ll11_opy_ = bstack1ll1l1_opy_ (u"ࠧࡴࡶࡤࡶࡹ࠭ᦊ")
  END = bstack1ll1l1_opy_ (u"ࠨࡧࡱࡨࠬᦋ")
  bstack1llll1l1_opy_ = bstack1ll1l1_opy_ (u"ࠩࡶ࡭ࡳ࡭࡬ࡦࠩᦌ")
bstack1llll11l1_opy_ = {
  bstack1ll1l1_opy_ (u"ࠪࡔ࡞࡚ࡅࡔࡖࠪᦍ"): bstack1ll1l1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫᦎ"),
  bstack1ll1l1_opy_ (u"ࠬࡖ࡙ࡕࡇࡖࡘ࠲ࡈࡄࡅࠩᦏ"): bstack1ll1l1_opy_ (u"࠭ࡐࡺࡶࡨࡷࡹ࠳ࡣࡶࡥࡸࡱࡧ࡫ࡲࠨᦐ")
}
PLAYWRIGHT_HUB_URL = bstack1ll1l1_opy_ (u"ࠢࡸࡵࡶ࠾࠴࠵ࡣࡥࡲ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡂࡧࡦࡶࡳ࠾ࠤᦑ")