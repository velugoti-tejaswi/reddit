import praw
from praw.models import MoreComments
from fastapi import APIRouter, Depends
from app.config import get_settings, Settings
from urllib.parse import quote_plus

router = APIRouter()


@router.get("/comments")
async def comments_list(settings: Settings = Depends(get_settings)):
	all_comments_list = []
	reply_text = ["I like this...", "Yes it's right...", "Yes"]
	reddit = praw.Reddit(
		client_id="j5iqV_4jCwApWOo4xWalAA",
		client_secret="jJf4NdM3VPHx2i3F6tD1n0BevL-8FA",
		user_agent="web:com.example.automatedcomment:v1.2.3 (by u/JaneJames0143)",
		username="JaneJames0143",
		password="Janejames@143",
		check_for_async=False
	)
	submission = reddit.submission(url="https://www.reddit.com/r/apexlegends/comments/rhyjbi/this_busted_underwater_hideout_feels_like_a_hack/")
	for top_level_comment in submission.comments:
		if isinstance(top_level_comment, MoreComments):
			continue
		if "lol" in top_level_comment.body.lower():
			authors_list = []
			for rep in top_level_comment.replies:
				authors_list.append(rep.author)
				if rep.author == "JaneJames0143":
					all_comments_list.append({"url":submission.url, "title":submission.title, "comment": top_level_comment.body,"reply": rep.body, "environment": settings.environment, "testing": settings.testing})
			if "JaneJames0143" not in authors_list:
				top_level_comment.reply(reply_text[0])
				all_comments_list.append({"url":submission.url, "title":submission.title, "comment": top_level_comment.body,"reply": reply_text[0], "environment": settings.environment, "testing": settings.testing})
		elif "water" in top_level_comment.body.lower():
			authors_list = []
			for rep in top_level_comment.replies:
				authors_list.append(rep.author)
				if rep.author == "JaneJames0143":
					all_comments_list.append({"url":submission.url, "title":submission.title, "comment": top_level_comment.body,"reply": rep.body, "environment": settings.environment, "testing": settings.testing})
			if "JaneJames0143" not in authors_list:
				top_level_comment.reply(reply_text[1])
				all_comments_list.append({"url":submission.url, "title":submission.title, "comment": top_level_comment.body,"reply": reply_text[1], "environment": settings.environment, "testing": settings.testing})
		elif "patched" in top_level_comment.body.lower():
			authors_list = []
			for rep in top_level_comment.replies:
				authors_list.append(rep.author)
				if rep.author == "JaneJames0143":
					all_comments_list.append({"url":submission.url, "title":submission.title, "comment": top_level_comment.body,"reply": rep.body, "environment": settings.environment, "testing": settings.testing})
			if "JaneJames0143" not in authors_list:
				top_level_comment.reply(reply_text[2])
				all_comments_list.append({"url":submission.url, "title":submission.title, "comment": top_level_comment.body,"reply": reply_text[2], "environment": settings.environment, "testing": settings.testing})
		else:
			all_comments_list.append({"url":submission.url, "title":submission.title, "comment": top_level_comment.body, "environment": settings.environment, "testing": settings.testing})
	for all_list in all_comments_list:
		all_list["id"] = all_comments_list.index(all_list) + 1
	return all_comments_list
