import os
import csv
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

# 유튜브 API 인증
scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
api_service_name = "youtube"
api_version = "v3"
client_secrets_file = "./client_secret.json"  # (중요) Google API Console에서 다운로드한 클라이언트 시크릿 파일

flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    client_secrets_file, scopes)
credentials = flow.run_local_server(port=8080)

youtube = googleapiclient.discovery.build(
    api_service_name, api_version, credentials=credentials)

video_id = ""  # (중요) 영상 ID


# 댓글과 좋아요 수 가져오기
def get_video_comments_with_likes(youtube, **kwargs):
    comments_with_likes = []
    request = youtube.commentThreads().list(
        **kwargs
    )

    while request:
        response = request.execute()
        for item in response["items"]:
            comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            like_count = item["snippet"]["topLevelComment"]["snippet"]["likeCount"]
            comments_with_likes.append((comment, like_count))

        request = youtube.commentThreads().list_next(request, response)

    return comments_with_likes


# 댓글 가져와 CSV 파일로 저장
def save_comments_to_csv(comments, file_path):
    with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["댓글", "좋아요 수"])  # 댓글과 좋아요 수 컬럼 추가
        sorted_comments = sorted(comments, key=lambda x: x[1], reverse=True)  # 좋아요 수에 따라 내림차순 정렬
        writer.writerows(sorted_comments)


# 댓글과 좋아요 수 가져오기
comments_with_likes = get_video_comments_with_likes(
    youtube,
    part="snippet",
    videoId=video_id,
    textFormat="plainText"
)

# CSV 파일로 저장
csv_file_path = video_id + ".csv"
save_comments_to_csv(comments_with_likes, csv_file_path)
print(f"댓글이 {csv_file_path}에 저장되었습니다.")