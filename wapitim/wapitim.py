from .__version__ import __version__
import subprocess
import json
import os
from urllib.parse import urlparse
from b_hunters.bhunter import BHunters
from karton.core import Task
import re
import os
from bson.objectid import ObjectId
# os.getenv("max_threads","400")
def parse_wapiti(file_path):
    results=[]
    with open(file_path, "r") as file:
        data = json.load(file)
    if "vulnerabilities" in data:
        print("Vulnerabilities found")
        for i in data["vulnerabilities"]:
            # print(i)
            for j in data["vulnerabilities"][i]:
                # print(j)
                results.append(f"Path:{j['path']} , info : {j['info']} , module: {i}")

    return results

class wapitim(BHunters):
    """
    B-Hunters Wapiti developed by Bormaa
    """

    identity = "B-Hunters-wapiti"
    version = __version__
    persistent = True
    filters = [
        {
            "type": "subdomain", "stage": "new"
        }
    ]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
    def wapiticommand(self,url):
        result=[]
        result403=[]
        newurls=[]
        outputfile=self.generate_random_filename()

        try:
            try:
                output = subprocess.run(["wapiti","-u",url,'-m',os.getenv("modules","backup,brute_login_form,cms,cookieflags,crlf,csp,csrf,exec,file,htaccess,htp,http_headers,https_redirect,ldap,log4shell,methods,network_device,nikto,permanentxss,redirect,shellshock,spring4shell,sql,ssl,ssrf,takeover,timesql,upload,wapp,wp_enum,xss,xxe"),'-f','json',"-o",outputfile],capture_output=True,text=True,timeout=10000, cwd='/')  
            except subprocess.TimeoutExpired:
                self.log.warning(f"Wapiti process timed out for URL: {url}")
            if os.path.exists(outputfile):
                result=parse_wapiti(outputfile)
                
                    
                os.remove(outputfile)

        except Exception as e:
            self.log.error("Error happened with xray")
            self.log.error(e)

            raise Exception(e)

        return result
                
    def scan(self,url):        
        result=self.wapiticommand(url)
        return result
        
    def process(self, task: Task) -> None:
        source = task.payload["source"]
        url =task.payload["data"]
        # if source == "producer":
        #     url = task.payload_persistent["domain"]
        # else:
        #     url = task.payload["data"]
        
        self.log.info("Starting processing new url")
        domain = re.sub(r'^https?://', '', url)
        domain = domain.rstrip('/')
        self.log.info(domain)
        self.scanid=task.payload_persistent["scan_id"]
        report_id=task.payload_persistent["report_id"]
        self.update_task_status(domain,"Started")
        try:
            result=self.scan(url)
            self.waitformongo()
            collection=self.db["reports"]
            if result !=[]:
                discorddata=[]
                for item in result:
                    # output = []
                    discorddata.append(item)
                discorddata="\n".join(discorddata)
                
                max_length = 4000
                discorddata_chunks = [discorddata[i:i + max_length] for i in range(0, len(discorddata), max_length)]
                
                for idx, chunk in enumerate(discorddata_chunks):
                    title = f"{self.identity} Results for {domain} (Part {idx + 1})" if len(discorddata_chunks) > 1 else f"{self.identity} Results for {domain}"
                    self.send_discord_webhook(title, chunk, "main")
                if self.db.client.is_primary:
                    update_result =collection.update_one({"_id": ObjectId(report_id)}, {"$push": {f"Vulns.Wapiti": {"$each": result}}})

                    if update_result.modified_count == 0:
                        self.log.warning(f"Update failed for domain {domain}. Document not found or no changes made.")
                        # Optionally, you can check if the document exists
                        if collection.count_documents({"Domain": domain}) == 0:
                            self.log.error(f"Document for domain {domain} does not exist in the collection.")
                        else:
                            self.log.info(f"Document exists for {domain}, but no changes were made. Possibly duplicate data.")
                    else:
                        self.log.info(f"Successfully updated document for domain {domain}")
                else:
                    raise Exception("MongoDB connection is not active. Update operation aborted.")

            self.update_task_status(domain,"Finished")
        except Exception as e:
            self.update_task_status(domain,"Failed")
            raise Exception(e)
            self.log.error(e)
