import argparse
import time
import mechanicalsoup

from google.cloud import pubsub_v1

def get_buganizer_info(browser, url):
    """Gather necessary Buganizer CR information. Currently returns entire page."""
    browser.open(url)
    return browser.get_current_page()


def get_callback(api_future, data, ref):
    """Wrap message data in the context of the callback function."""
    def callback(api_future):
        try:
            print("Published message {} now has message ID {}".format(data, api_future.result()))
            ref["num_messages"] += 1
        except Exception:
            print("A problem occured when publishing {}: {}\n".format(data, api_future.exception()))
            raise
    return callback

def pub(project_id, topic_name, message):
    """Publish a message to a Pub/Sub topic."""
    client = pubsub_v1.PublisherClient()
    topic_path = client.topic_path(project_id, topic_name)
    data = message.encode()
    ref = dict({"num_messages": 0})

    api_future = client.publish(topic_path, data=data)
    api_future.add_done_callback(get_callback(api_future, data, ref))

    while api_future.running():
        time.sleep(0.5)
        print("Published {} message(s).".format(ref["num_messages"]))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("project_id", help="Google Cloud project ID")
    parser.add_argument("topic_name", help="Pub/Sub topic name")

    args = parser.parse_args()

    browser = mechanicalsoup.StatefulBrowser()
    url = "https://b.corp.google.com/issues/156748140" #Temporarily hardcoding URL
    message = get_buganizer_info(browser, url)

    pub(args.project_id, args.topic_name, message)
