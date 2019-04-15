from locust import HttpLocust, TaskSet, task


# extend from TaskSet
class UserBehavior(TaskSet):
    # define tasks to perform
    @task
    def view_incident(self):
        self.client.get("http://ec2-54-254-185-54.ap-southeast-1.compute.amazonaws.com/incident/1")
    @task
    def view_all_pendingIncidents(self):
        self.client.get("http://ec2-54-254-185-54.ap-southeast-1.compute.amazonaws.com/allIncidents", data = {"status": ["Pending"], "order": "Desc"})



class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    # max wait time between the execution of locust tasks
    min_wait = 1
    # min wait time between the execution of locust tasks
    max_wait = 5

    #throughput = no of request/total ime