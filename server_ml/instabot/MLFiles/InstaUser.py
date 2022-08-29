class User:
    def __init__(self, user_biography_length, user_follower_count, user_following_count, user_has_profile_pic,
                 user_is_private, user_media_count, username_digit_count, username_length, mediaUpload_times,
                 media_comment_numbers, media_has_location_info,
                 media_hashtag_numbers, media_like_numbers,  user_has_external_url, user_has_highlight_reels,
                 user_tags_count):
        self.user_biography_length = user_biography_length
        self.user_follower_count = user_follower_count
        self.user_following_count = user_following_count
        self.user_has_profile_pic = user_has_profile_pic
        self.user_is_private = user_is_private
        self.user_media_count = user_media_count
        self.username_digit_count = username_digit_count
        self.username_length = username_length
        self.follower_following_ratio = user_follower_count / \
            max(1, user_following_count)
        self.mediaUpload_times = mediaUpload_times
        self.media_comment_numbers = media_comment_numbers
        self.media_has_location_info = media_has_location_info
        self.media_hashtag_numbers = media_hashtag_numbers
        self.media_like_numbers = media_like_numbers
        self.user_has_external_url = user_has_external_url
        self.user_has_highlight_reels = user_has_highlight_reels
        self.user_tags_count = user_tags_count


""""
User Properties:
user_biography_length
user_follower_count
user_following_count
user_has_profile_pic
user_is_private
user_media_count
username_digit_count
username_length
follower_following_ratio
mediaUpload_times
media_comment_numbers
media_has_location_info
media_hashtag_numbers
media_like_numbers
user_has_external_url
user_has_highlight_reels
user_tags_count
"""
