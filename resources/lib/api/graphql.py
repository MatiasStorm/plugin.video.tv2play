import requests
from .models.video import Video
from .models.serie import Serie
from resources.lib.logging import LOG

class GraphQL_API():
    def __init__(self):
        self.api_url = "https://api.ovp.tv2.dk"
        self.COMEDY_ID = "U3RydWN0dXJlOnVybMKke2NvbnRlbnR9L3Byb2dyYW1zL3Nlcmllcz9jYXRlZ29yeT1Db21lZHl8dGl0bGXCpENvbWVkeXxwcmVzZW50YXRpb27CpGZpbHRlcnBhbmVsfHBsYXRmb3JtwqR1bmRlZmluZWR8b3B0aW9uwqR1bmRlZmluZWQ="

    def __get_headers(self, access_token):
        headers = {
                "Authorization": access_token
        }
        return headers

    def get_video(self, guid, client_id, access_token):
        query = """query  {
          playback(
            guid: "%s"
            format: ["application/dash+xml"]
            platform: play_web
          ) {
            subtitles {
              useAsDefault
            }
            progress {
              position
            }
            pid
            smil(clientId: "%s") {
              video {
                src
                type
              }
              securityLicense {
                url
                token
              }
            }
          }
        }""" % ( guid, client_id )
        headers = self.__get_headers(access_token)
        response = requests.post(self.api_url, json={"query": query }, headers=headers)
        if response.status_code == 200:
            return Video(response.json()["data"])
        return None

    def get_series(self, category_id):
        sort = "popular"
        query = """query play_web_content_Structure(
              $entitySort: SortType
              $structureId: ID!
              $limit: Int
            ) {
              structure(id: $structureId) {
                ...StructureFragment
              }
            }
            fragment StructureFragment on Structure {
              entities(
                sort: $entitySort
                limit: $limit
              ) {
                pageInfo {
                  totalCount
                }
                nodes {
                  ...StructureEntityFragment
                }
              }
            }

            fragment StructureEntityFragment on Entity {
              id
              guid
              type
              title: presentationTitle
              description: presentationDescription
              thumbnail: presentationArt {
                type
                url
              }
              ... on Episode {
                art(type: "promotion") {
                  nodes {
                    url
                    watermarkParam
                  }
                }
              }
            }
        """
        variables = {"limit": 9999, "entitySort": sort, "structureId": category_id}
        data = {"query": query, "variables": variables}
        response = requests.post(self.api_url, json=data)
        if response.status_code == 200:
            series = []
            for s in response.json()["data"]["structure"]["entities"]["nodes"]:
                series.append(Serie(s))
            return series
        return None



