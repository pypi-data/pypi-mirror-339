# coding: UTF-8
import sys
bstack11111ll_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack111_opy_ = 7
def bstack11l1l11_opy_ (bstack11lll_opy_):
    global bstack1l11l11_opy_
    bstack1l1l1_opy_ = ord (bstack11lll_opy_ [-1])
    bstack1l111ll_opy_ = bstack11lll_opy_ [:-1]
    bstack11l_opy_ = bstack1l1l1_opy_ % len (bstack1l111ll_opy_)
    bstack11l111l_opy_ = bstack1l111ll_opy_ [:bstack11l_opy_] + bstack1l111ll_opy_ [bstack11l_opy_:]
    if bstack11111ll_opy_:
        bstack1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1l1l11_opy_ + bstack1l1l1_opy_) % bstack111_opy_) for bstack1l1l11_opy_, char in enumerate (bstack11l111l_opy_)])
    else:
        bstack1l_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1l1l11_opy_ + bstack1l1l1_opy_) % bstack111_opy_) for bstack1l1l11_opy_, char in enumerate (bstack11l111l_opy_)])
    return eval (bstack1l_opy_)
import os
from urllib.parse import urlparse
from bstack_utils.config import Config
from bstack_utils.messages import bstack11l1l11lll1_opy_
bstack111ll1lll_opy_ = Config.bstack111l1l1l_opy_()
def bstack111lll1lll1_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack111llll111l_opy_(bstack111llll1111_opy_, bstack111llll11l1_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack111llll1111_opy_):
        with open(bstack111llll1111_opy_) as f:
            pac = PACFile(f.read())
    elif bstack111lll1lll1_opy_(bstack111llll1111_opy_):
        pac = get_pac(url=bstack111llll1111_opy_)
    else:
        raise Exception(bstack11l1l11_opy_ (u"ࠬࡖࡡࡤࠢࡩ࡭ࡱ࡫ࠠࡥࡱࡨࡷࠥࡴ࡯ࡵࠢࡨࡼ࡮ࡹࡴ࠻ࠢࡾࢁࠬᱵ").format(bstack111llll1111_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack11l1l11_opy_ (u"ࠨ࠸࠯࠺࠱࠼࠳࠾ࠢᱶ"), 80))
        bstack111lll1llll_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack111lll1llll_opy_ = bstack11l1l11_opy_ (u"ࠧ࠱࠰࠳࠲࠵࠴࠰ࠨᱷ")
    proxy_url = session.get_pac().find_proxy_for_url(bstack111llll11l1_opy_, bstack111lll1llll_opy_)
    return proxy_url
def bstack1l1ll1ll11_opy_(config):
    return bstack11l1l11_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫᱸ") in config or bstack11l1l11_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ᱹ") in config
def bstack11ll1l1l1_opy_(config):
    if not bstack1l1ll1ll11_opy_(config):
        return
    if config.get(bstack11l1l11_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭ᱺ")):
        return config.get(bstack11l1l11_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧᱻ"))
    if config.get(bstack11l1l11_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩᱼ")):
        return config.get(bstack11l1l11_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪᱽ"))
def bstack1ll11lll1_opy_(config, bstack111llll11l1_opy_):
    proxy = bstack11ll1l1l1_opy_(config)
    proxies = {}
    if config.get(bstack11l1l11_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪ᱾")) or config.get(bstack11l1l11_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬ᱿")):
        if proxy.endswith(bstack11l1l11_opy_ (u"ࠩ࠱ࡴࡦࡩࠧᲀ")):
            proxies = bstack11llll1l_opy_(proxy, bstack111llll11l1_opy_)
        else:
            proxies = {
                bstack11l1l11_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩᲁ"): proxy
            }
    bstack111ll1lll_opy_.bstack11l111l1_opy_(bstack11l1l11_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡖࡩࡹࡺࡩ࡯ࡩࡶࠫᲂ"), proxies)
    return proxies
def bstack11llll1l_opy_(bstack111llll1111_opy_, bstack111llll11l1_opy_):
    proxies = {}
    global bstack111llll11ll_opy_
    if bstack11l1l11_opy_ (u"ࠬࡖࡁࡄࡡࡓࡖࡔ࡞࡙ࠨᲃ") in globals():
        return bstack111llll11ll_opy_
    try:
        proxy = bstack111llll111l_opy_(bstack111llll1111_opy_, bstack111llll11l1_opy_)
        if bstack11l1l11_opy_ (u"ࠨࡄࡊࡔࡈࡇ࡙ࠨᲄ") in proxy:
            proxies = {}
        elif bstack11l1l11_opy_ (u"ࠢࡉࡖࡗࡔࠧᲅ") in proxy or bstack11l1l11_opy_ (u"ࠣࡊࡗࡘࡕ࡙ࠢᲆ") in proxy or bstack11l1l11_opy_ (u"ࠤࡖࡓࡈࡑࡓࠣᲇ") in proxy:
            bstack111lll1ll1l_opy_ = proxy.split(bstack11l1l11_opy_ (u"ࠥࠤࠧᲈ"))
            if bstack11l1l11_opy_ (u"ࠦ࠿࠵࠯ࠣᲉ") in bstack11l1l11_opy_ (u"ࠧࠨᲊ").join(bstack111lll1ll1l_opy_[1:]):
                proxies = {
                    bstack11l1l11_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬ᲋"): bstack11l1l11_opy_ (u"ࠢࠣ᲌").join(bstack111lll1ll1l_opy_[1:])
                }
            else:
                proxies = {
                    bstack11l1l11_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧ᲍"): str(bstack111lll1ll1l_opy_[0]).lower() + bstack11l1l11_opy_ (u"ࠤ࠽࠳࠴ࠨ᲎") + bstack11l1l11_opy_ (u"ࠥࠦ᲏").join(bstack111lll1ll1l_opy_[1:])
                }
        elif bstack11l1l11_opy_ (u"ࠦࡕࡘࡏ࡙࡛ࠥᲐ") in proxy:
            bstack111lll1ll1l_opy_ = proxy.split(bstack11l1l11_opy_ (u"ࠧࠦࠢᲑ"))
            if bstack11l1l11_opy_ (u"ࠨ࠺࠰࠱ࠥᲒ") in bstack11l1l11_opy_ (u"ࠢࠣᲓ").join(bstack111lll1ll1l_opy_[1:]):
                proxies = {
                    bstack11l1l11_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧᲔ"): bstack11l1l11_opy_ (u"ࠤࠥᲕ").join(bstack111lll1ll1l_opy_[1:])
                }
            else:
                proxies = {
                    bstack11l1l11_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩᲖ"): bstack11l1l11_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧᲗ") + bstack11l1l11_opy_ (u"ࠧࠨᲘ").join(bstack111lll1ll1l_opy_[1:])
                }
        else:
            proxies = {
                bstack11l1l11_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬᲙ"): proxy
            }
    except Exception as e:
        print(bstack11l1l11_opy_ (u"ࠢࡴࡱࡰࡩࠥ࡫ࡲࡳࡱࡵࠦᲚ"), bstack11l1l11lll1_opy_.format(bstack111llll1111_opy_, str(e)))
    bstack111llll11ll_opy_ = proxies
    return proxies