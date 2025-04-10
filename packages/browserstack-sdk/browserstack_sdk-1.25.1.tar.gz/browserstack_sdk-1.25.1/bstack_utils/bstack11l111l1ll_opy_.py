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
from uuid import uuid4
from bstack_utils.helper import bstack11l1ll11ll_opy_, bstack11l1ll11lll_opy_
from bstack_utils.bstack1l1l111ll_opy_ import bstack111l1l1l1ll_opy_
class bstack111lll1ll1_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, started_at=None, framework=None, tags=[], scope=[], bstack111l1111111_opy_=None, bstack1111lllllll_opy_=True, bstack1l11l11ll11_opy_=None, bstack1lllllll11_opy_=None, result=None, duration=None, bstack111l1ll1l1_opy_=None, meta={}):
        self.bstack111l1ll1l1_opy_ = bstack111l1ll1l1_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack1111lllllll_opy_:
            self.uuid = uuid4().__str__()
        self.started_at = started_at
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack111l1111111_opy_ = bstack111l1111111_opy_
        self.bstack1l11l11ll11_opy_ = bstack1l11l11ll11_opy_
        self.bstack1lllllll11_opy_ = bstack1lllllll11_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
        self.hooks = []
    def bstack111ll11111_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack11l111l111_opy_(self, meta):
        self.meta = meta
    def bstack111llll1ll_opy_(self, hooks):
        self.hooks = hooks
    def bstack111l111l1l1_opy_(self):
        bstack111l111l111_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack1ll1l1_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨᶩ"): bstack111l111l111_opy_,
            bstack1ll1l1_opy_ (u"࠭࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࠨᶪ"): bstack111l111l111_opy_,
            bstack1ll1l1_opy_ (u"ࠧࡷࡥࡢࡪ࡮ࡲࡥࡱࡣࡷ࡬ࠬᶫ"): bstack111l111l111_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack1ll1l1_opy_ (u"ࠣࡗࡱࡩࡽࡶࡥࡤࡶࡨࡨࠥࡧࡲࡨࡷࡰࡩࡳࡺ࠺ࠡࠤᶬ") + key)
            setattr(self, key, val)
    def bstack111l1111ll1_opy_(self):
        return {
            bstack1ll1l1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᶭ"): self.name,
            bstack1ll1l1_opy_ (u"ࠪࡦࡴࡪࡹࠨᶮ"): {
                bstack1ll1l1_opy_ (u"ࠫࡱࡧ࡮ࡨࠩᶯ"): bstack1ll1l1_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬᶰ"),
                bstack1ll1l1_opy_ (u"࠭ࡣࡰࡦࡨࠫᶱ"): self.code
            },
            bstack1ll1l1_opy_ (u"ࠧࡴࡥࡲࡴࡪࡹࠧᶲ"): self.scope,
            bstack1ll1l1_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭ᶳ"): self.tags,
            bstack1ll1l1_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬᶴ"): self.framework,
            bstack1ll1l1_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᶵ"): self.started_at
        }
    def bstack1111lllll1l_opy_(self):
        return {
         bstack1ll1l1_opy_ (u"ࠫࡲ࡫ࡴࡢࠩᶶ"): self.meta
        }
    def bstack111l111l11l_opy_(self):
        return {
            bstack1ll1l1_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡗ࡫ࡲࡶࡰࡓࡥࡷࡧ࡭ࠨᶷ"): {
                bstack1ll1l1_opy_ (u"࠭ࡲࡦࡴࡸࡲࡤࡴࡡ࡮ࡧࠪᶸ"): self.bstack111l1111111_opy_
            }
        }
    def bstack111l11111ll_opy_(self, bstack111l1111l1l_opy_, details):
        step = next(filter(lambda st: st[bstack1ll1l1_opy_ (u"ࠧࡪࡦࠪᶹ")] == bstack111l1111l1l_opy_, self.meta[bstack1ll1l1_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᶺ")]), None)
        step.update(details)
    def bstack11lll1ll1l_opy_(self, bstack111l1111l1l_opy_):
        step = next(filter(lambda st: st[bstack1ll1l1_opy_ (u"ࠩ࡬ࡨࠬᶻ")] == bstack111l1111l1l_opy_, self.meta[bstack1ll1l1_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᶼ")]), None)
        step.update({
            bstack1ll1l1_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᶽ"): bstack11l1ll11ll_opy_()
        })
    def bstack111llll11l_opy_(self, bstack111l1111l1l_opy_, result, duration=None):
        bstack1l11l11ll11_opy_ = bstack11l1ll11ll_opy_()
        if bstack111l1111l1l_opy_ is not None and self.meta.get(bstack1ll1l1_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᶾ")):
            step = next(filter(lambda st: st[bstack1ll1l1_opy_ (u"࠭ࡩࡥࠩᶿ")] == bstack111l1111l1l_opy_, self.meta[bstack1ll1l1_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭᷀")]), None)
            step.update({
                bstack1ll1l1_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭᷁"): bstack1l11l11ll11_opy_,
                bstack1ll1l1_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱ᷂ࠫ"): duration if duration else bstack11l1ll11lll_opy_(step[bstack1ll1l1_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ᷃")], bstack1l11l11ll11_opy_),
                bstack1ll1l1_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ᷄"): result.result,
                bstack1ll1l1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭᷅"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack111l11111l1_opy_):
        if self.meta.get(bstack1ll1l1_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬ᷆")):
            self.meta[bstack1ll1l1_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭᷇")].append(bstack111l11111l1_opy_)
        else:
            self.meta[bstack1ll1l1_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧ᷈")] = [ bstack111l11111l1_opy_ ]
    def bstack1111lllll11_opy_(self):
        return {
            bstack1ll1l1_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ᷉"): self.bstack111ll11111_opy_(),
            **self.bstack111l1111ll1_opy_(),
            **self.bstack111l111l1l1_opy_(),
            **self.bstack1111lllll1l_opy_()
        }
    def bstack111l111111l_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack1ll1l1_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ᷊"): self.bstack1l11l11ll11_opy_,
            bstack1ll1l1_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡡࡰࡷࠬ᷋"): self.duration,
            bstack1ll1l1_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ᷌"): self.result.result
        }
        if data[bstack1ll1l1_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭᷍")] == bstack1ll1l1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪ᷎ࠧ"):
            data[bstack1ll1l1_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫᷏ࠧ")] = self.result.bstack1111ll1l11_opy_()
            data[bstack1ll1l1_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧ᷐ࠪ")] = [{bstack1ll1l1_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭᷑"): self.result.bstack11l1lll11ll_opy_()}]
        return data
    def bstack111l1111lll_opy_(self):
        return {
            bstack1ll1l1_opy_ (u"ࠫࡺࡻࡩࡥࠩ᷒"): self.bstack111ll11111_opy_(),
            **self.bstack111l1111ll1_opy_(),
            **self.bstack111l111l1l1_opy_(),
            **self.bstack111l111111l_opy_(),
            **self.bstack1111lllll1l_opy_()
        }
    def bstack111ll11l1l_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack1ll1l1_opy_ (u"࡙ࠬࡴࡢࡴࡷࡩࡩ࠭ᷓ") in event:
            return self.bstack1111lllll11_opy_()
        elif bstack1ll1l1_opy_ (u"࠭ࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨᷔ") in event:
            return self.bstack111l1111lll_opy_()
    def bstack111l11llll_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack1l11l11ll11_opy_ = time if time else bstack11l1ll11ll_opy_()
        self.duration = duration if duration else bstack11l1ll11lll_opy_(self.started_at, self.bstack1l11l11ll11_opy_)
        if result:
            self.result = result
class bstack11l11111l1_opy_(bstack111lll1ll1_opy_):
    def __init__(self, hooks=[], bstack11l111llll_opy_={}, *args, **kwargs):
        self.hooks = hooks
        self.bstack11l111llll_opy_ = bstack11l111llll_opy_
        super().__init__(*args, **kwargs, bstack1lllllll11_opy_=bstack1ll1l1_opy_ (u"ࠧࡵࡧࡶࡸࠬᷕ"))
    @classmethod
    def bstack111l111l1ll_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack1ll1l1_opy_ (u"ࠨ࡫ࡧࠫᷖ"): id(step),
                bstack1ll1l1_opy_ (u"ࠩࡷࡩࡽࡺࠧᷗ"): step.name,
                bstack1ll1l1_opy_ (u"ࠪ࡯ࡪࡿࡷࡰࡴࡧࠫᷘ"): step.keyword,
            })
        return bstack11l11111l1_opy_(
            **kwargs,
            meta={
                bstack1ll1l1_opy_ (u"ࠫ࡫࡫ࡡࡵࡷࡵࡩࠬᷙ"): {
                    bstack1ll1l1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᷚ"): feature.name,
                    bstack1ll1l1_opy_ (u"࠭ࡰࡢࡶ࡫ࠫᷛ"): feature.filename,
                    bstack1ll1l1_opy_ (u"ࠧࡥࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬᷜ"): feature.description
                },
                bstack1ll1l1_opy_ (u"ࠨࡵࡦࡩࡳࡧࡲࡪࡱࠪᷝ"): {
                    bstack1ll1l1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᷞ"): scenario.name
                },
                bstack1ll1l1_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᷟ"): steps,
                bstack1ll1l1_opy_ (u"ࠫࡪࡾࡡ࡮ࡲ࡯ࡩࡸ࠭ᷠ"): bstack111l1l1l1ll_opy_(test)
            }
        )
    def bstack111l111ll1l_opy_(self):
        return {
            bstack1ll1l1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫᷡ"): self.hooks
        }
    def bstack1111llllll1_opy_(self):
        if self.bstack11l111llll_opy_:
            return {
                bstack1ll1l1_opy_ (u"࠭ࡩ࡯ࡶࡨ࡫ࡷࡧࡴࡪࡱࡱࡷࠬᷢ"): self.bstack11l111llll_opy_
            }
        return {}
    def bstack111l1111lll_opy_(self):
        return {
            **super().bstack111l1111lll_opy_(),
            **self.bstack111l111ll1l_opy_()
        }
    def bstack1111lllll11_opy_(self):
        return {
            **super().bstack1111lllll11_opy_(),
            **self.bstack1111llllll1_opy_()
        }
    def bstack111l11llll_opy_(self):
        return bstack1ll1l1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࠩᷣ")
class bstack11l11l111l_opy_(bstack111lll1ll1_opy_):
    def __init__(self, hook_type, *args,bstack11l111llll_opy_={}, **kwargs):
        self.hook_type = hook_type
        self.bstack111l111ll11_opy_ = None
        self.bstack11l111llll_opy_ = bstack11l111llll_opy_
        super().__init__(*args, **kwargs, bstack1lllllll11_opy_=bstack1ll1l1_opy_ (u"ࠨࡪࡲࡳࡰ࠭ᷤ"))
    def bstack111ll1ll11_opy_(self):
        return self.hook_type
    def bstack111l1111l11_opy_(self):
        return {
            bstack1ll1l1_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬᷥ"): self.hook_type
        }
    def bstack111l1111lll_opy_(self):
        return {
            **super().bstack111l1111lll_opy_(),
            **self.bstack111l1111l11_opy_()
        }
    def bstack1111lllll11_opy_(self):
        return {
            **super().bstack1111lllll11_opy_(),
            bstack1ll1l1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤ࡯ࡤࠨᷦ"): self.bstack111l111ll11_opy_,
            **self.bstack111l1111l11_opy_()
        }
    def bstack111l11llll_opy_(self):
        return bstack1ll1l1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳ࠭ᷧ")
    def bstack111llllll1_opy_(self, bstack111l111ll11_opy_):
        self.bstack111l111ll11_opy_ = bstack111l111ll11_opy_