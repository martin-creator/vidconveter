import pika, json, tempfile, os
from bson.objectid import ObjectId
import moviepy.editor  # moviepy is used to convert video to mp3

def start(message, fs_videos, fs_mp3s, channel):
    message = json.loads(message)

    # empty temp file
    tf = tempfile.NamedTemporaryFile()
    # videp contents
    out = fs_videos.get(ObjectId(message["video_fid"]))
    # add contents to empty file
    tf.write(out.read())
    # create moviepy clip
    audio = moviepy.editor.VideoFileClip(tf.name).audio
    tf.close()

    # write audio to file
    tf_path = tempfile.gettempdir() + f"/{message['video_fid']}.mp3"
    audio.write_audiofile(tf_path)

    # save file to mongo
    f = open(tf_path, "rb")
    data = f.read()
    fid = fs_mp3.put(data)
    f.close()
    os.remove(tf_path)

    message["mp3_fid"] = str(fid)

    try:
        channel.basic_publish(
            exchange="",
            routing_key=os.environ.get("MP3_QUEUE"),
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE,
            ),
        )
    except Exception as e:
        fs_mp3s.delete(fid)
        return "failed to publish to mp3 queue"