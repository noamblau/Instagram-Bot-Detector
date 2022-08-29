from instaloader import Instaloader, Profile
from MLFiles.InstaUser import User
from PIL import Image
import requests


# check if the color of the pixle is white or grey
def check_color(r, g, b, color):
    COLOR = 219
    if color == "white":
        COLOR = 255
    if r == COLOR and g == COLOR and b == COLOR:
        return True
    return False


# if the picture has pixles of grey and white in specific pixles user doesn't have profile pic
def profile_pic(profile):
    img = Image.open(requests.get(profile.profile_pic_url, stream=True).raw)
    img.convert('RGB')
    r1, g1, b1 = img.getpixel((0, 0))
    r2, g2, b2 = img.getpixel(tuple([img.size[0]/4, img.size[1]/4]))
    if check_color(r1, g1, b1, "white") and check_color(r2, g2, b2, "grey"):
        return 0
    return 1


# create user instance for username
def build_user(account_to_predict, username, password):
    try:
        L = Instaloader()
        L.login(username, password)
        # if username doesn't exist raise ProfileNotExistsException
        profile = Profile.from_username(L.context, account_to_predict)
    except Exception as e:
        print(f"Error: {e}")
        return None

    print("Login successful.")
    print("Building user:")
    print("-Getting general details...")
    user_biography_length = len(profile.biography)
    user_follower_count = profile.followers
    user_following_count = profile.followees
    print("-Getting profile pic...")
    user_has_profile_pic = profile_pic(profile)
    print("-Getting additional details...")
    user_is_private = int(profile.is_private)
    user_media_count = profile.mediacount
    username_digit_count = sum(c.isdigit() for c in profile.username)
    username_length = len(profile.username)
    user_has_external_url = 0
    if profile.external_url:
        user_has_external_url = 1
    user_has_highlight_reels = int(profile.has_highlight_reels)
    print("-Getting tagged posts...")
    user_tags_count = len(list(profile.get_tagged_posts()))
    mediaUpload_times = []
    media_comment_numbers = []
    media_has_location_info = []
    media_hashtag_numbers = []
    media_like_numbers = []
    print("-Getting posts...")
    posts = list(profile.get_posts())
    for i in range(min(len(posts), 5)):
        p = posts[i]
        mediaUpload_times.append(int(p.date.timestamp()))
        media_comment_numbers.append(p.comments)
        if p.location:
            media_has_location_info.append(1)
        else:
            media_has_location_info.append(0)
        media_hashtag_numbers.append(len(p.caption_hashtags))
        media_like_numbers.append(p.likes)

    print("Done building user")
    return User(user_biography_length,
                user_follower_count,
                user_following_count,
                user_has_profile_pic,
                user_is_private,
                user_media_count,
                username_digit_count,
                username_length,
                mediaUpload_times,
                media_comment_numbers,
                media_has_location_info,
                media_hashtag_numbers,
                media_like_numbers,
                user_has_external_url,
                user_has_highlight_reels,
                user_tags_count)
