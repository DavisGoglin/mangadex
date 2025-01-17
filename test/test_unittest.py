"""
Module for unittesting
"""
from pathlib import Path
import json
import pytest
import mangadex as md


def read_json_files(filename: str, mode: str = "r") -> dict:
    with open(filename, mode) as f:
        resp = json.load(f)
    return resp


USER_DATA_DIR = Path("test/user_data.txt")


class TestApi:
    api = md.Api()
    timeout = 5

    def test_mangaList(self):
        self.api.get_manga_list(limit=1)[0]

    def test_SearchManga(self):
        # we're going to search for the iris zero
        resp = self.api.get_manga_list(title="iris zero", limit=1)[0]

        url = f"{self.api.URL}/manga"
        raw_response = md.URLRequest.request_url(
            url, "GET", timeout=self.timeout, params={"limit": 1, "title": "iris zero"}
        )

        saved_resp = md.Manga.manga_from_dict(raw_response["data"][0])

        assert resp == saved_resp, "The Manga objects are not equal"

    def test_SerachMangaWithLotOfArgs(self):
        tags = self.api.tag_list()
        wanted_tags = ["Oneshot", "Romance"]
        not_wanted_tags = ["Loli", "Incest"]
        wanted_tags_ids = []
        not_wanted_tags_ids = []
        for i, t in enumerate(tags):
            if t.name["en"] in wanted_tags:
                wanted_tags_ids.append(t.tag_id)
            elif t.name["en"] in not_wanted_tags:
                not_wanted_tags_ids.append(t.tag_id)

        manga_list = self.api.get_manga_list(
            contentRating=["erotica", "pornographic"],
            status=["completed"],
            excludedTags=not_wanted_tags_ids,
            excludedTagsMode="AND",
            includedTags=wanted_tags_ids,
            includedTagsMode="AND",
        )

    def test_RandomManga(self):
        self.api.random_manga()

    def test_GetMangaChapter(self):
        ch_id = "015979c8-ffa4-4afa-b48e-3da6d10279b0"
        resp = self.api.get_chapter(chapter_id=ch_id)

        url = f"{self.api.URL}/chapter/{ch_id}"
        raw_response = md.URLRequest.request_url(
            url, "GET", timeout=self.timeout, params={"id": ch_id}
        )

        saved_resp = md.Chapter.chapter_from_dict(raw_response)

        assert resp == saved_resp, "The Chapter Objects are not equal"

    def test_FetchChapterImages(self):
        ch_id = "015979c8-ffa4-4afa-b48e-3da6d10279b0"

        resp = self.api.get_chapter(chapter_id=ch_id)

        resp.fetch_chapter_images()

    def test_GetAuthor(self):

        author_id = "df765fdc-ea9f-45d0-9191-d95615662d49"

        resp = self.api.get_author_by_id(author_id=author_id)

        url = f"{self.api.URL}/author/{author_id}"

        raw_response = md.URLRequest.request_url(
            url, "GET", timeout=self.timeout, params={"id": author_id}
        )

        saved_resp = md.Author.author_from_dict(raw_response)

        assert resp == saved_resp, "The Author Objects are not equal"

    def test_GetAuthorPlural(self):
        author_ids = [
            "df765fdc-ea9f-45d0-9191-d95615662d49",
            "742bea86-c1ae-4893-bd06-805287991849",
        ]

        resp = self.api.get_author(ids=author_ids)

        url = f"{self.api.URL}/author/?ids[]={author_ids[0]}&ids[]={author_ids[1]}"
        raw_response = md.URLRequest.request_url(url, "GET", timeout=self.timeout)

        manual_authors = [
            md.Author.author_from_dict(author) for author in raw_response["data"]
        ]
        manual_authors = dict(((author.author_id, author) for author in manual_authors))

        for author in author_ids:
            api_author = next((a for a in resp if a.author_id == author), None)
            assert api_author is not None, "Required author not returned in response"
            assert (
                api_author == manual_authors[author]
            ), "The Author Objects are not equal"

    def test_GetTags(self):
        resp = self.api.tag_list()

        url = f"{self.api.URL}/manga/tag"
        raw_response = md.URLRequest.request_url(url, "GET", timeout=self.timeout)
        saved_reps = md.Tag.create_tag_list(raw_response)

        assert resp == saved_reps, "The test objects are not equal"

    def test_GetMangaChaptersAndVolumes(self):
        # lets use iris zero as is in hiatus
        manga_id = "786ff721-8fd3-413d-8e50-938d8b06f917"
        resp = self.api.get_manga_volumes_and_chapters(manga_id=manga_id)

        url = f"{self.api.URL}/manga/{manga_id}/aggregate"

        raw_response = md.URLRequest.request_url(url, "GET", timeout=self.timeout)

        saved_resp = raw_response["volumes"]

        assert resp == saved_resp, "The values are not equal"

    def test_GetScanlationGroup(self):
        ids = ["f5f83084-ec42-4354-96fd-1b637a89b8b3"]
        resp = self.api.scanlation_group_list(group_ids=ids)  # black cat scanlations

        url = f"{self.api.URL}/group"
        raw_response = md.URLRequest.request_url(
            url, "GET", timeout=self.timeout, params={"ids[]": ids}
        )

        saved_response = md.ScanlationGroup.create_group_list(raw_response)

        assert resp == saved_response

    @pytest.mark.skipif(
        not USER_DATA_DIR.exists(),
        reason=f"The directory {USER_DATA_DIR} is not present",
    )
    def test_GetUser(self):
        with open("test/user_data.txt", "r") as f:
            user_id = f.readline().strip("\n")
            username = f.readline().strip("\n")
        user = self.api.get_user(user_id=user_id)

        assert user.username == username, "This user is invalid"

    def test_GetCoverArtList(self):
        self.api.get_coverart_list()

    def test_GetMangaCoverArt(self):
        random_manga = self.api.random_manga()
        self.api.get_cover(random_manga.cover_id)

    @pytest.mark.skipif(
        not USER_DATA_DIR.exists(),
        reason=f"The directory {USER_DATA_DIR} is not present",
    )
    def test_GetUserCustomLists(self):
        with open("test/user_data.txt", "r") as f:
            user_id = f.readline().strip("\n")

        self.api.get_user_customlists(user_id)


CREDENTIALS = Path("test/credentials.txt")


@pytest.mark.skipif(
    not CREDENTIALS.exists(), reason=f"The directory {CREDENTIALS} is not present"
)
class Test_private_api:
    api = md.Api()
    timeout = 5

    def login(self):
        credentials = read_json_files(CREDENTIALS)
        self.api.login(credentials["username"], credentials["password"])

    def test_GetMangaReadingStatus(self):
        self.login()

        manga_id = "35c33279-395d-4d9f-abec-93893c28ab29"
        self.api.get_manga_read_markes(manga_id=manga_id)

    def test_GetAllMangaReadingStatus(self):
        self.login()

        self.api.get_all_manga_reading_status()

    def test_GetMyMangaList(self):
        self.login()
        self.api.get_my_mangalist()

    def test_FollowManga(self):
        manga_id = "32d76d19-8a05-4db0-9fc2-e0b0648fe9d0"  # solo leveling

        self.login()

        self.api.follow_manga(manga_id=manga_id)

    def test_UnfollowManga(self):
        manga_id = "32d76d19-8a05-4db0-9fc2-e0b0648fe9d0"  # solo leveling

        self.login()

        self.api.unfollow_manga(manga_id=manga_id)

    def test_GetMyCustomLists(self):
        self.login()

        self.api.get_my_customlists()
