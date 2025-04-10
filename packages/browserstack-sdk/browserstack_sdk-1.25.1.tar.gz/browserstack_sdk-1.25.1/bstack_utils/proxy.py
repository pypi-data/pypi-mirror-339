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
from urllib.parse import urlparse
from bstack_utils.config import Config
from bstack_utils.messages import bstack11l111l1l11_opy_
bstack11ll11ll_opy_ = Config.bstack1l11l1l1ll_opy_()
def bstack111l1ll1l1l_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack111l1ll1l11_opy_(bstack111l1lll1l1_opy_, bstack111l1lll111_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack111l1lll1l1_opy_):
        with open(bstack111l1lll1l1_opy_) as f:
            pac = PACFile(f.read())
    elif bstack111l1ll1l1l_opy_(bstack111l1lll1l1_opy_):
        pac = get_pac(url=bstack111l1lll1l1_opy_)
    else:
        raise Exception(bstack1ll1l1_opy_ (u"ࠨࡒࡤࡧࠥ࡬ࡩ࡭ࡧࠣࡨࡴ࡫ࡳࠡࡰࡲࡸࠥ࡫ࡸࡪࡵࡷ࠾ࠥࢁࡽࠨᴄ").format(bstack111l1lll1l1_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack1ll1l1_opy_ (u"ࠤ࠻࠲࠽࠴࠸࠯࠺ࠥᴅ"), 80))
        bstack111l1ll1ll1_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack111l1ll1ll1_opy_ = bstack1ll1l1_opy_ (u"ࠪ࠴࠳࠶࠮࠱࠰࠳ࠫᴆ")
    proxy_url = session.get_pac().find_proxy_for_url(bstack111l1lll111_opy_, bstack111l1ll1ll1_opy_)
    return proxy_url
def bstack11l1llll1l_opy_(config):
    return bstack1ll1l1_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧᴇ") in config or bstack1ll1l1_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩᴈ") in config
def bstack11ll11l1_opy_(config):
    if not bstack11l1llll1l_opy_(config):
        return
    if config.get(bstack1ll1l1_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩᴉ")):
        return config.get(bstack1ll1l1_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪᴊ"))
    if config.get(bstack1ll1l1_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬᴋ")):
        return config.get(bstack1ll1l1_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ᴌ"))
def bstack111ll1l1_opy_(config, bstack111l1lll111_opy_):
    proxy = bstack11ll11l1_opy_(config)
    proxies = {}
    if config.get(bstack1ll1l1_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭ᴍ")) or config.get(bstack1ll1l1_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨᴎ")):
        if proxy.endswith(bstack1ll1l1_opy_ (u"ࠬ࠴ࡰࡢࡥࠪᴏ")):
            proxies = bstack1l1111l1l_opy_(proxy, bstack111l1lll111_opy_)
        else:
            proxies = {
                bstack1ll1l1_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬᴐ"): proxy
            }
    bstack11ll11ll_opy_.bstack1ll11111_opy_(bstack1ll1l1_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡙ࡥࡵࡶ࡬ࡲ࡬ࡹࠧᴑ"), proxies)
    return proxies
def bstack1l1111l1l_opy_(bstack111l1lll1l1_opy_, bstack111l1lll111_opy_):
    proxies = {}
    global bstack111l1ll1lll_opy_
    if bstack1ll1l1_opy_ (u"ࠨࡒࡄࡇࡤࡖࡒࡐ࡚࡜ࠫᴒ") in globals():
        return bstack111l1ll1lll_opy_
    try:
        proxy = bstack111l1ll1l11_opy_(bstack111l1lll1l1_opy_, bstack111l1lll111_opy_)
        if bstack1ll1l1_opy_ (u"ࠤࡇࡍࡗࡋࡃࡕࠤᴓ") in proxy:
            proxies = {}
        elif bstack1ll1l1_opy_ (u"ࠥࡌ࡙࡚ࡐࠣᴔ") in proxy or bstack1ll1l1_opy_ (u"ࠦࡍ࡚ࡔࡑࡕࠥᴕ") in proxy or bstack1ll1l1_opy_ (u"࡙ࠧࡏࡄࡍࡖࠦᴖ") in proxy:
            bstack111l1lll11l_opy_ = proxy.split(bstack1ll1l1_opy_ (u"ࠨࠠࠣᴗ"))
            if bstack1ll1l1_opy_ (u"ࠢ࠻࠱࠲ࠦᴘ") in bstack1ll1l1_opy_ (u"ࠣࠤᴙ").join(bstack111l1lll11l_opy_[1:]):
                proxies = {
                    bstack1ll1l1_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨᴚ"): bstack1ll1l1_opy_ (u"ࠥࠦᴛ").join(bstack111l1lll11l_opy_[1:])
                }
            else:
                proxies = {
                    bstack1ll1l1_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࠪᴜ"): str(bstack111l1lll11l_opy_[0]).lower() + bstack1ll1l1_opy_ (u"ࠧࡀ࠯࠰ࠤᴝ") + bstack1ll1l1_opy_ (u"ࠨࠢᴞ").join(bstack111l1lll11l_opy_[1:])
                }
        elif bstack1ll1l1_opy_ (u"ࠢࡑࡔࡒ࡜࡞ࠨᴟ") in proxy:
            bstack111l1lll11l_opy_ = proxy.split(bstack1ll1l1_opy_ (u"ࠣࠢࠥᴠ"))
            if bstack1ll1l1_opy_ (u"ࠤ࠽࠳࠴ࠨᴡ") in bstack1ll1l1_opy_ (u"ࠥࠦᴢ").join(bstack111l1lll11l_opy_[1:]):
                proxies = {
                    bstack1ll1l1_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࠪᴣ"): bstack1ll1l1_opy_ (u"ࠧࠨᴤ").join(bstack111l1lll11l_opy_[1:])
                }
            else:
                proxies = {
                    bstack1ll1l1_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬᴥ"): bstack1ll1l1_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣᴦ") + bstack1ll1l1_opy_ (u"ࠣࠤᴧ").join(bstack111l1lll11l_opy_[1:])
                }
        else:
            proxies = {
                bstack1ll1l1_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨᴨ"): proxy
            }
    except Exception as e:
        print(bstack1ll1l1_opy_ (u"ࠥࡷࡴࡳࡥࠡࡧࡵࡶࡴࡸࠢᴩ"), bstack11l111l1l11_opy_.format(bstack111l1lll1l1_opy_, str(e)))
    bstack111l1ll1lll_opy_ = proxies
    return proxies