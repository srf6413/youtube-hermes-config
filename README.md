<!--* freshness: { owner: 'victorngo' reviewed: '2020-05-04' } *-->

# YouTube Hermes Config Automation

Replace YouTube Hermes configuration tools with buganizer driven automation.

Run Instructions:

pip install mechanicalsoup
export PROJECT='google.com:youtube-admin-pacing-server'
python pub.py $PROJECT BuganizerCR
