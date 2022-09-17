from app.api.base.controller import BaseController
from app.api.v1.endpoints.user.repository import repos_profile


class CtrUser(BaseController):
    async def ctr_profile(self, user_id):
        profile_res = self.call_repos(await repos_profile(user_id=user_id))
        return self.response(data=profile_res)
