# mangadex

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A python wrapper for the mangadex API V5. It uses the requests library and all the aditional arguments can be viewed in the [Official Mangadex Documentation](https://api.mangadex.org/docs.html)

## Instaling the API

### PyPI

```sh
pip install --Upgrade mangadex
```

### Installing via setuptools

```sh
python setup.py install --user
```

## Using the API

```py
>>> import mangadex
>>> api = mangadex.Api()
```

## Public Calls

### Getting the latest manga

This is called mangalist in the [documentation](https://api.mangadex.org/docs.html#operation/get-search-manga)

```py
>>> manga_list = api.get_manga_list(limit = 1) #limits the query to return just one manga
>>> manga_list[Manga(manga_id = 0001183c-2089-48e9-96b7-d48db5f1a611, title = {'en': 'Eight'}, altTitles = [{'ja': '8（エイト）'}], description = {'en': 'Tokyo in the 90s, the city center has been suffering from a continuing depopulation. Also affected is the Udagawa Junior High School where only six people are left, as their class leader, protector and very good friend Masato just died in an illegal skateboarding race. Five months later Eito Hachiya, nickname: Eight or "8" enrolls in school and wants to find out what happened. He even just looks like Masato! But mysteries surround him: Why does he know all the other six? Why can’t they remember him?  \n  \nNote: Was cancelled after ~25% of volume 4, the epilogue consists of an alternative ending for Eight.'}, isLocked = False, links = {'al': '38734', 'ap': 'eight', 'kt': '17709', 'mu': '6521', 'amz': 'https://www.amazon.co.jp/dp/B07WS2K894', 'mal': '8734', 'raw': 'https://csbs.shogakukan.co.jp/book?book_group_id=14478'}, originalLanguage = ja
 lastVolume = 4, lastChapter = 37.6, publicationDemographic = seinen, status = completed, year = 2000, contentRating = safe
 createdAt = 2018-02-04 21:32:02+00:00, uploadedAt = 2022-01-12 21:42:40+00:00), author_id = ['905aaced-1556-4925-bff0-14ea277fb0b1', '905aaced-1556-4925-bff0-14ea277fb0b1'], artist_id = [], cover_id = 51bf2e88-98ac-4fd7-afb5-80edff694d53
```

You can also use the `get_manga_list()` method to search for manga.

The usage is like this

```py
>>> manga_list = api.get_manga_list(title = "You manga title here")
```

~~**NOTE**: The search rigth now is faulty but tahts is an api problem. At the moment the only parameters that work are: `title`, `limit` and `offset`~~

The search is now working so the above is no longer true

### Getting a manga by its id

```py
>>> manga = api.view_manga_by_id(manga_id = "0001183c-2089-48e9-96b7-d48db5f1a611")
```

### Random manga

```py
>>> random_manga = api.random_manga()
```

### Manga Feed

Get the chapter, or chapters from the feed of a specific manga.

```py
>>> manga_feed = api.manga_feed(manga_id = "0001183c-2089-48e9-96b7-d48db5f1a611", limit = 1)
[Chapter(chapter_id = 015979c8-ffa4-4afa-b48e-3da6d10279b0, title = Navel-Gazing, volume = 3, chapter = 23.0, translatedLanguage = en, hash =
 data = List[filenames], publishAt = 2018-03-19 01:32:00+00:00, createdAt = 2018-03-19 01:32:00+00:00, uploadedAt = 2018-03-19 01:32:00+00:00, group_id = 59957a04-fa91-4099-921d-7e7988a19acb, manga_id = 0001183c-2089-48e9-96b7-d48db5f1a611, uploader = e19519ce-8c5f-4d7c-8280-704a87d34429)]
```

### Get manga volumnes and chapters

Get a manga volumes and chapters

```py
>>> api.get_manga_volumes_and_chapters(manga_id = "the manga id")
```

### Get Chapter

Returns a Chpater Object  by its id

```py
>>> chapter = api.get_chapter(chapter_id = "015979c8-ffa4-4afa-b48e-3da6d10279b0")
>> chapter
Chapter(chapter_id = 015979c8-ffa4-4afa-b48e-3da6d10279b0, title = Navel-Gazing, volume = 3, chapter = 23.0, translatedLanguage = en, hash =
data = List[filenames], publishAt = 2018-03-19 01:32:00+00:00, createdAt = 2018-03-19 01:32:00+00:00, uploadedAt = 2018-03-19 01:32:00+00:00, group_id = 59957a04-fa91-4099-921d-7e7988a19acb, manga_id = 0001183c-2089-48e9-96b7-d48db5f1a611, uploader = e19519ce-8c5f-4d7c-8280-704a87d34429)
```

### Chapter List

It will return a list of chapters

```py
>>> chapter_list = api.chapter_list()
```

If you want the chpaters of a given Manga, you'll need to specify the [feed endpoints](https://api.mangadex.org/docs.html#operation/get-search-group)

### Chapter Images

Return the links for the chapter images for a given Chapter Object. This is a Chapter method

```py
>>> Chapter.fetch_chapter_images()
```

### Get User

Get a User by id

```py
>>> user = api.get_user(user_id = "id of user")
```

### Tag List

The list of the manga tags

```py
>>> tag_list = api.tag_list()
```

### Get scanlation group list

Get a Scanlation Group list

```py
>>> api.scanlation_group_list()
```

### Cover Images List

Get the cover image list

```py
>>> api.get_coverart_list()
```

### Get Cover by Id

```py
>>> api.get_cover(cover_id = "the cover id")
```

### Edit Cover

```py
>>> api.edit_cover(cover_id = "the cover id", description = "the cover description, can be null", volume = "the volume number", version = "int, the cover version")
```

### Get cover image link

```py
>>> CoverArt.fetch_cover_image()
```

This is a CoverArt method that returns the cover image url of that object

### Create account

To create an account

```py
>>> api.create_account(username = "your username", password = "your password", email = "youremail@example.com", ObjReturn = False)
```

This will send you an activation code, this is the one to pass to `activate_account`.

```py
>>> api.acticate_account(code = "the code sent")
```

If you need another activation code:

```py
>>> api.resend_activation_code(email = "anotheremail@example.com")
```

### Account recovery

To recover and account

```py
>> api.recover_account(email = "youremail@example.com")
```

This will send you and activation code that you need

```py
>>> api.complete_account_recover(code = "the code sent to you", newPassword = "the new password for the account")
```

## Private Calls

### Login

Method to login to the website

```py
>>> api.login(username = USERNAME, password = PASSWORD)
```

It is recomended that you add this values to you path for security reasons.

### Your User Info

Get your user info

```py
>>> my_user = api.me()
```

### Get Logged User Followed Manga List

Get your manga follow list!

```py
>>> follow_list = api.get_my_mangalist()
```

This functions, as well as most of the other ones accept optional parameters.
This are:

* `limit` : limits the amout of results. It accepts a value between 1 and 100, the default if 10
* `offset` : Makes an offset of the velue provided to the list. Accepts values >= 0

### Get Logged User Followed Groups

Get the list of the Scanlination group you follow!

```py
>>> scangroups_followlist = api.get_my_followed_groups()
```

### Get Logged User Followed Users

The list of the users you follow

```py
>>> followed_users = api.get_my_followed_users()
```

### Get chapters marked as read from a manga

Get a list of the capters marked as read for a given manga

```py
>>> read_chapters = api.get_manga_read_markes(id = "the manga id")
```

### Get all followed manga reading status

Get a list of the all the manga reading stauts

```py
>>> my_manga_reading_stauts = api.get_all_manga_reading_status()
```

### Get a specific manga reading status

Get the reading status of a specific manga

```py
>>> manga_reading_status = api.get_manga_reading_status(manga_id = "the manga id")
```

### Update Manga reading status

```py
>>> api.update_manga_reading_status(manga_id = "the manga id", status = "the new reading status")
```

The `status` parameter can take the following values:
`"reading"` `"on_hold"` `"plan_to_read"` `"dropped"` `"re_reading"` `"completed"`

### Follow a manga

Follow a manga

```py
>>> api.follow_manga(manga_id = "the manga id")
```

### Unfollow a manga

Unfollows a manga

```py
>>>api.unfollow_manga(manga_id = "the manga id")
```

### Create manga

Creates a manga

```py
>>> api.create_manga(title = "manga title", )
```

### Update Manga

Updates a manga

```py
>>> api.update_manga(manga_id = "the manga id")
```

### Delete Manga

Deletes manga

```py
>>> api.delete_manga(manga_id = "the manga id")
```

### Add manga to custom list

Add a manga to a custom list

```py
>>> api.add_manga_to_customlist(manga_id = "the manga id", list_id = "the list id")
```

### Remove a manga from custom list

Removes a manga from a custom list

```py
>>> api.remove_manga_from_customlist(id = "the manga id", listId = "the list id")
```

### Create  a custom list

```py
>>> api.create_customlist() #this will create a custom list with no special parameters
```

#### Query parameters

* `name`. The custom list name
* `visibility`. The visibility of the custom list. Default public
* `manga`. The list of manga ids

### Get custom list

```py
>>> api.get_customlist(id = "th custom list id")
```

### Update custom list

```py
>>> api.update_customlist(id = "the custom list id")
```

#### Query parameters

* `name`. The custom list name
* `visibility`. Values : `"public"` `"private"`

### Delete custom list

```py
>>> api.delete_customlist(id = "the custom list id")
```

### Get User Custom list

```py
>>> api.get_user_customlists(id = "the user id")
```

#### QueryParams

* `limit`. The limit of custom lists to return
* `offset`. The amout of offset

### Create Author

```py
>>> api.create_author(name = "author name", version = 1, ObjReturn = False)
```

### Update Author

```py
>>> api.update_author(id = "the author id", version = "int with the version", name = "author's name", ObjReturn = False)
```

### Delete Author

```py
>>> api.delete_author(id = "the author id")
```

### Discalimer

All the credit for the API goes to the Mangadex Team.
