from app.api.base.repository import ReposReturn


# todo ví dụ data response
async def repos_profile(user_id) -> ReposReturn:
    return ReposReturn(data={
        "user_id": f"{user_id}",
        "username": "dev1",
        "name": "Developer 1",
        "code": "192323",
        "avatar_url": "cdn/users/avatar/dev1.jpg",
        "token": "5deb5d337c8ae85564717dde65f4861930ae5c75",
        "email": "thanghd@scb.com.vn"
    })
