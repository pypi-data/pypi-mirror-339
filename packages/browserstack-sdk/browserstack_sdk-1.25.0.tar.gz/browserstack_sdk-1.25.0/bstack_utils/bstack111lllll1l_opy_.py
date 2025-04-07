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
from uuid import uuid4
from bstack_utils.helper import bstack1ll11ll11_opy_, bstack11ll1ll1ll1_opy_
from bstack_utils.bstack1lll11lll1_opy_ import bstack111lll1l1l1_opy_
class bstack111ll1l111_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, started_at=None, framework=None, tags=[], scope=[], bstack111l1lll111_opy_=None, bstack111ll1111ll_opy_=True, bstack1l11ll1l11l_opy_=None, bstack1ll1ll1ll_opy_=None, result=None, duration=None, bstack111l1llll1_opy_=None, meta={}):
        self.bstack111l1llll1_opy_ = bstack111l1llll1_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack111ll1111ll_opy_:
            self.uuid = uuid4().__str__()
        self.started_at = started_at
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack111l1lll111_opy_ = bstack111l1lll111_opy_
        self.bstack1l11ll1l11l_opy_ = bstack1l11ll1l11l_opy_
        self.bstack1ll1ll1ll_opy_ = bstack1ll1ll1ll_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
        self.hooks = []
    def bstack111ll11111_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack11l11l1111_opy_(self, meta):
        self.meta = meta
    def bstack111lllll11_opy_(self, hooks):
        self.hooks = hooks
    def bstack111l1ll1l1l_opy_(self):
        bstack111l1ll1ll1_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack11l1l11_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬᴚ"): bstack111l1ll1ll1_opy_,
            bstack11l1l11_opy_ (u"ࠪࡰࡴࡩࡡࡵ࡫ࡲࡲࠬᴛ"): bstack111l1ll1ll1_opy_,
            bstack11l1l11_opy_ (u"ࠫࡻࡩ࡟ࡧ࡫࡯ࡩࡵࡧࡴࡩࠩᴜ"): bstack111l1ll1ll1_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack11l1l11_opy_ (u"࡛ࠧ࡮ࡦࡺࡳࡩࡨࡺࡥࡥࠢࡤࡶ࡬ࡻ࡭ࡦࡰࡷ࠾ࠥࠨᴝ") + key)
            setattr(self, key, val)
    def bstack111l1lllll1_opy_(self):
        return {
            bstack11l1l11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᴞ"): self.name,
            bstack11l1l11_opy_ (u"ࠧࡣࡱࡧࡽࠬᴟ"): {
                bstack11l1l11_opy_ (u"ࠨ࡮ࡤࡲ࡬࠭ᴠ"): bstack11l1l11_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩᴡ"),
                bstack11l1l11_opy_ (u"ࠪࡧࡴࡪࡥࠨᴢ"): self.code
            },
            bstack11l1l11_opy_ (u"ࠫࡸࡩ࡯ࡱࡧࡶࠫᴣ"): self.scope,
            bstack11l1l11_opy_ (u"ࠬࡺࡡࡨࡵࠪᴤ"): self.tags,
            bstack11l1l11_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩᴥ"): self.framework,
            bstack11l1l11_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫᴦ"): self.started_at
        }
    def bstack111l1llll11_opy_(self):
        return {
         bstack11l1l11_opy_ (u"ࠨ࡯ࡨࡸࡦ࠭ᴧ"): self.meta
        }
    def bstack111ll111l1l_opy_(self):
        return {
            bstack11l1l11_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡔࡨࡶࡺࡴࡐࡢࡴࡤࡱࠬᴨ"): {
                bstack11l1l11_opy_ (u"ࠪࡶࡪࡸࡵ࡯ࡡࡱࡥࡲ࡫ࠧᴩ"): self.bstack111l1lll111_opy_
            }
        }
    def bstack111l1ll1lll_opy_(self, bstack111ll111111_opy_, details):
        step = next(filter(lambda st: st[bstack11l1l11_opy_ (u"ࠫ࡮ࡪࠧᴪ")] == bstack111ll111111_opy_, self.meta[bstack11l1l11_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᴫ")]), None)
        step.update(details)
    def bstack1l1lll11l1_opy_(self, bstack111ll111111_opy_):
        step = next(filter(lambda st: st[bstack11l1l11_opy_ (u"࠭ࡩࡥࠩᴬ")] == bstack111ll111111_opy_, self.meta[bstack11l1l11_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᴭ")]), None)
        step.update({
            bstack11l1l11_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᴮ"): bstack1ll11ll11_opy_()
        })
    def bstack11l11l1l1l_opy_(self, bstack111ll111111_opy_, result, duration=None):
        bstack1l11ll1l11l_opy_ = bstack1ll11ll11_opy_()
        if bstack111ll111111_opy_ is not None and self.meta.get(bstack11l1l11_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᴯ")):
            step = next(filter(lambda st: st[bstack11l1l11_opy_ (u"ࠪ࡭ࡩ࠭ᴰ")] == bstack111ll111111_opy_, self.meta[bstack11l1l11_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᴱ")]), None)
            step.update({
                bstack11l1l11_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᴲ"): bstack1l11ll1l11l_opy_,
                bstack11l1l11_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࠨᴳ"): duration if duration else bstack11ll1ll1ll1_opy_(step[bstack11l1l11_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫᴴ")], bstack1l11ll1l11l_opy_),
                bstack11l1l11_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᴵ"): result.result,
                bstack11l1l11_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪᴶ"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack111ll11111l_opy_):
        if self.meta.get(bstack11l1l11_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᴷ")):
            self.meta[bstack11l1l11_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᴸ")].append(bstack111ll11111l_opy_)
        else:
            self.meta[bstack11l1l11_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᴹ")] = [ bstack111ll11111l_opy_ ]
    def bstack111ll111ll1_opy_(self):
        return {
            bstack11l1l11_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᴺ"): self.bstack111ll11111_opy_(),
            **self.bstack111l1lllll1_opy_(),
            **self.bstack111l1ll1l1l_opy_(),
            **self.bstack111l1llll11_opy_()
        }
    def bstack111ll1111l1_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack11l1l11_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᴻ"): self.bstack1l11ll1l11l_opy_,
            bstack11l1l11_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࡢ࡭ࡳࡥ࡭ࡴࠩᴼ"): self.duration,
            bstack11l1l11_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᴽ"): self.result.result
        }
        if data[bstack11l1l11_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᴾ")] == bstack11l1l11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᴿ"):
            data[bstack11l1l11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠫᵀ")] = self.result.bstack1111ll1lll_opy_()
            data[bstack11l1l11_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧᵁ")] = [{bstack11l1l11_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪᵂ"): self.result.bstack11lll111l11_opy_()}]
        return data
    def bstack111ll111l11_opy_(self):
        return {
            bstack11l1l11_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᵃ"): self.bstack111ll11111_opy_(),
            **self.bstack111l1lllll1_opy_(),
            **self.bstack111l1ll1l1l_opy_(),
            **self.bstack111ll1111l1_opy_(),
            **self.bstack111l1llll11_opy_()
        }
    def bstack111llll1l1_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack11l1l11_opy_ (u"ࠩࡖࡸࡦࡸࡴࡦࡦࠪᵄ") in event:
            return self.bstack111ll111ll1_opy_()
        elif bstack11l1l11_opy_ (u"ࠪࡊ࡮ࡴࡩࡴࡪࡨࡨࠬᵅ") in event:
            return self.bstack111ll111l11_opy_()
    def bstack111ll111l1_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack1l11ll1l11l_opy_ = time if time else bstack1ll11ll11_opy_()
        self.duration = duration if duration else bstack11ll1ll1ll1_opy_(self.started_at, self.bstack1l11ll1l11l_opy_)
        if result:
            self.result = result
class bstack11l1111111_opy_(bstack111ll1l111_opy_):
    def __init__(self, hooks=[], bstack11l111l11l_opy_={}, *args, **kwargs):
        self.hooks = hooks
        self.bstack11l111l11l_opy_ = bstack11l111l11l_opy_
        super().__init__(*args, **kwargs, bstack1ll1ll1ll_opy_=bstack11l1l11_opy_ (u"ࠫࡹ࡫ࡳࡵࠩᵆ"))
    @classmethod
    def bstack111l1llll1l_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack11l1l11_opy_ (u"ࠬ࡯ࡤࠨᵇ"): id(step),
                bstack11l1l11_opy_ (u"࠭ࡴࡦࡺࡷࠫᵈ"): step.name,
                bstack11l1l11_opy_ (u"ࠧ࡬ࡧࡼࡻࡴࡸࡤࠨᵉ"): step.keyword,
            })
        return bstack11l1111111_opy_(
            **kwargs,
            meta={
                bstack11l1l11_opy_ (u"ࠨࡨࡨࡥࡹࡻࡲࡦࠩᵊ"): {
                    bstack11l1l11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᵋ"): feature.name,
                    bstack11l1l11_opy_ (u"ࠪࡴࡦࡺࡨࠨᵌ"): feature.filename,
                    bstack11l1l11_opy_ (u"ࠫࡩ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠩᵍ"): feature.description
                },
                bstack11l1l11_opy_ (u"ࠬࡹࡣࡦࡰࡤࡶ࡮ࡵࠧᵎ"): {
                    bstack11l1l11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᵏ"): scenario.name
                },
                bstack11l1l11_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᵐ"): steps,
                bstack11l1l11_opy_ (u"ࠨࡧࡻࡥࡲࡶ࡬ࡦࡵࠪᵑ"): bstack111lll1l1l1_opy_(test)
            }
        )
    def bstack111l1lll11l_opy_(self):
        return {
            bstack11l1l11_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨᵒ"): self.hooks
        }
    def bstack111l1lll1ll_opy_(self):
        if self.bstack11l111l11l_opy_:
            return {
                bstack11l1l11_opy_ (u"ࠪ࡭ࡳࡺࡥࡨࡴࡤࡸ࡮ࡵ࡮ࡴࠩᵓ"): self.bstack11l111l11l_opy_
            }
        return {}
    def bstack111ll111l11_opy_(self):
        return {
            **super().bstack111ll111l11_opy_(),
            **self.bstack111l1lll11l_opy_()
        }
    def bstack111ll111ll1_opy_(self):
        return {
            **super().bstack111ll111ll1_opy_(),
            **self.bstack111l1lll1ll_opy_()
        }
    def bstack111ll111l1_opy_(self):
        return bstack11l1l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳ࠭ᵔ")
class bstack11l111llll_opy_(bstack111ll1l111_opy_):
    def __init__(self, hook_type, *args,bstack11l111l11l_opy_={}, **kwargs):
        self.hook_type = hook_type
        self.bstack111l1lll1l1_opy_ = None
        self.bstack11l111l11l_opy_ = bstack11l111l11l_opy_
        super().__init__(*args, **kwargs, bstack1ll1ll1ll_opy_=bstack11l1l11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪᵕ"))
    def bstack111l11llll_opy_(self):
        return self.hook_type
    def bstack111l1llllll_opy_(self):
        return {
            bstack11l1l11_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩᵖ"): self.hook_type
        }
    def bstack111ll111l11_opy_(self):
        return {
            **super().bstack111ll111l11_opy_(),
            **self.bstack111l1llllll_opy_()
        }
    def bstack111ll111ll1_opy_(self):
        return {
            **super().bstack111ll111ll1_opy_(),
            bstack11l1l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡ࡬ࡨࠬᵗ"): self.bstack111l1lll1l1_opy_,
            **self.bstack111l1llllll_opy_()
        }
    def bstack111ll111l1_opy_(self):
        return bstack11l1l11_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࠪᵘ")
    def bstack11l11l11ll_opy_(self, bstack111l1lll1l1_opy_):
        self.bstack111l1lll1l1_opy_ = bstack111l1lll1l1_opy_