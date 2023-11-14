from sqlalchemy import insert, select, delete

from db import db
from models import ApisRepoCommit, Api
from app import app
from services.embedding import getembeddings
from services.public_apis_github_repo_service import getlastcommitdata, getapischangesinapisrepo
from services.extract_apis_data_from_readme import crawl_apis_from_repo
from dateutil import parser as date_parser
from utils.iter import find

@app.cli.command()
def update_apis_table():
  last_commit_in_db = db.session.execute(
    select(ApisRepoCommit) \
    .order_by( ApisRepoCommit.commit_timestamp.desc() )
    .limit(1)
  ).scalar()
  last_commit_in_db_sha = last_commit_in_db.sha
  repo_current_last_commit = getlastcommitdata()
  repo_current_last_commit_sha = repo_current_last_commit.get('sha')

  if repo_current_last_commit_sha == last_commit_in_db_sha: return

  apis_changes = getapischangesinapisrepo(last_commit_in_db_sha,repo_current_last_commit_sha)


  added_apis = apis_changes.get('added')
  removed_apis = apis_changes.get('removed')

  # Complete APIs data with categories and embeddings

  # Categories
  apis_in_latest_version_dict = dict(
    [ (x['url'],x) for x in crawl_apis_from_repo(repo_current_last_commit_sha) ]
  )
  apis_to_add = [
    api | {'category': apis_in_latest_version_dict[ api['url'] ]['category'] }
    for api in added_apis if apis_in_latest_version_dict.get(api['url'])
  ]

  # Embeddings
  embeddings_iter = getembeddings([x['description'] for x in apis_to_add ])
  apis_to_add = [
    api | {'embedding': embedding }
    for api, embedding in zip(apis_to_add,embeddings_iter)
  ]
  
  # Now perform the DB operations
  # Delete APIs that were removed from the repo
  db.session.execute(
    delete(Api).where( 
      Api.url.in_( [x['url'] for x in removed_apis ] )
    )
  )

  # Add new APIs 
  db.session.execute(insert(Api),apis_to_add)

  # # Keep track of last commit in the repo
  db.session.execute(
    insert( ApisRepoCommit ),
    [
      {
        'commit_timestamp': date_parser.parse(repo_current_last_commit['commit']['author']['date']),
        'sha': repo_current_last_commit_sha
      }
    ]
  )
  db.session.commit()

update_apis_table()
