import launch

if not launch.is_installed("tweepy"):
    launch.run_pip("install tweepy", "tweepy")
