# from flight import Flight
from heap import Heap, comp1, comp2


class Planner:
    def __init__(self, flights):
        """The Planner

        Args:
            flights (List[Flight]): A list of information of all the flights (objects of class Flight)
        """
        self.flights = self.fn(flights)
        self.n = self.no_of_cities(flights)
        self.adj_by_city = self.adj_list(self.flights)
        self.adj_by_flight = self.adj2(self.flights)
        pass

    def fn(self, l):
        l1 = [None] * len(l)
        for i in l:
            l1[i.flight_no] = i
        return l1

    def no_of_cities(self, l):
        mx = 0
        for i in l:
            mx = max(mx, i.start_city, i.end_city)
        return mx + 1

    def adj_list(self, l):
        adj = [[] for i in range(self.n)]
        for i in l:
            adj[i.start_city].append(i)
        return adj

    def adj2(self, l):
        # list1-->city i me konsi flights aa rahi hai.
        list1 = [[] for i in range(self.n)]
        for i in l:  # O(m)
            list1[i.end_city].append(i.flight_no)
        ans = [[] for i in range(len(l))]
        for i in l:  # O(m)
            for j in list1[i.start_city]:  # O(n)
                if i.departure_time >= self.flights[j].arrival_time + 20:
                    ans[j].append(i)
        return ans

    def least_flights_earliest_route(self, start_city, end_city, t1, t2):
        """
        Return List[Flight]: A route from start_city to end_city, which departs after t1 (>= t1) and
        arrives before t2 (<=) satisfying:
        The route has the least number of flights, and within routes with same number of flights,
        arrives the earliest
        """
        if start_city==end_city:
            return []
        queue=[]
        for i in self.adj_by_city[start_city]:
            if i.departure_time>=t1 and i.arrival_time<=t2:
                queue.append(i)
        level=[]
        prev=[None]*len(self.adj_by_flight)
        is_visited=False
        last=None
        best_time= float('inf')
        while queue:
            for f in queue:
                if is_visited==True:
                    if f.end_city==end_city:
                        if f.arrival_time<best_time:
                            best_time=f.arrival_time
                            last=f
                    continue
                if f.end_city==end_city:
                    is_visited=True
                    last=f
                    best_time=f.arrival_time
                else:
                    for i in self.adj_by_flight[f.flight_no]:
                        if i.arrival_time<=t2:
                            level.append(i)
                            prev[i.flight_no]=(f,1)

            if last:
                return self.reconstruct_path(prev,last)

            queue=level
            level=[]

        return []

        # if start_city==end_city:
        #     return []
        # arrival_time = [None] * len(self.adj_by_city)
        # prev_flight = [None] * len(self.adj_by_city)
        # dist = [float('inf') for i in range(len(self.adj_by_flight))]
        # q = Queue()
        #
        # for i in self.adj_by_city[start_city]:
        #     if i.departure_time >= t1 and i.arrival_time <= t2:
        #         if arrival_time[i.end_city] is None:
        #             arrival_time[i.end_city] = i.arrival_time
        #             dist[i.flight_no] = 0
        #             prev_flight[i.end_city] = i
        #             q.enqueue(i.end_city)
        #         elif arrival_time[i.end_city] > i.arrival_time:
        #             arrival_time[i.end_city] = i.arrival_time
        #             prev_flight[i.end_city] = i
        #             dist[i.flight_no] = 0
        # while not q.isempty():
        #     c = q.dequeue()
        #     f = prev_flight[c]
        #     if c == end_city:
        #         ans = [f]
        #         v = f.start_city
        #         while v != start_city:
        #             ans.append(prev_flight[v])
        #             v = prev_flight[v].start_city
        #         ans.reverse()
        #         return ans
        #     for i in self.adj_by_flight[f.flight_no]:
        #         if i.arrival_time <= t2:
        #             if arrival_time[i.end_city] is None:
        #                 arrival_time[i.end_city] = i.arrival_time
        #                 dist[i.flight_no] = dist[f.flight_no] + 1
        #                 prev_flight[i.end_city] = i
        #                 q.enqueue(i.end_city)
        #             elif dist[f.flight_no] + 1 <= dist[i.flight_no] and i.arrival_time < arrival_time[i.end_city]:
        #                 arrival_time[i.end_city] = i.arrival_time
        #                 arrival_time[i.end_city] = i.arrival_time
        #                 dist[i.flight_no] = dist[f.flight_no] + 1
        #                 prev_flight[i.end_city] = i
        #                 q.enqueue(i.end_city)
        # return []



    def reconstruct_path(self, l, lf):
        ans = [lf]
        v = lf
        while v != None and l[v.flight_no] != None:
            ans.append(l[v.flight_no][0])
            v = l[v.flight_no][0]
        ans.reverse()
        return ans

    def cheapest_route(self, start_city, end_city, t1, t2):
        """
        Return List[Flight]: A route from start_city to end_city, which departs after t1 (>= t1) and
        arrives before t2 (<=) satisfying:
        The route is a cheapest route
        """
        if start_city==end_city:
            return []
        arr = []
        for i in self.adj_by_city[start_city]:
            if i.departure_time >= t1:
                arr.append((i.fare, i))
        pre = [None] * len(self.flights)
        finalflight = None
        h = Heap(comp1, arr)
        while len(h.data)>0:
            fare, f = h.extract()
            if f.end_city == end_city and f.arrival_time <= t2:
                finalflight = f
                return self.reconstruct_path(pre, finalflight)
            for i in self.adj_by_flight[f.flight_no]:
                if i.arrival_time <= t2:
                    if pre[i.flight_no] == None:
                        pre[i.flight_no] = (f, fare)
                        h.insert((i.fare + fare, i))
                    elif fare < pre[i.flight_no][1]:
                        pre[i.flight_no] = (f, fare)
                        h.insert((i.fare + fare, i))

    def least_flights_cheapest_route(self, start_city, end_city, t1, t2):
        """
        Return List[Flight]: A route from start_city to end_city, which departs after t1 (>= t1) and
        arrives before t2 (<=) satisfying:
        The route has the least number of flights, and within routes with same number of flights,
        is the cheapest
        """
        if start_city==end_city:
            return []
        queue=[]
        for i in self.adj_by_city[start_city]:
            if i.departure_time>=t1 and i.arrival_time<=t2:
                queue.append((i.fare,i))
        level=[]
        prev=[None]*len(self.adj_by_flight)
        is_visited=False
        last=None
        best_fare= float('inf')
        while queue:
            for fare, f in queue:
                if is_visited==True:
                    if f.end_city==end_city:
                        if fare<best_fare:
                            best_fare=fare
                            last=f
                    continue
                if f.end_city==end_city:
                    is_visited=True
                    last=f
                    best_fare=fare
                else:
                    for i in self.adj_by_flight[f.flight_no]:
                        if i.arrival_time<=t2:
                            level.append((i.fare+fare,i))
                            prev[i.flight_no]=(f,fare)

            if last:
                return self.reconstruct_path(prev,last)

            queue=level
            level=[]

        return []

        # arr = []
        # for i in self.adj_by_city[start_city]:
        #     if i.departure_time >= t1:
        #         arr.append((0, i.fare, i))
        # pre = [None] * len(self.flights)
        # dist = [float('inf') for i in range(len(self.adj_by_flight))]
        # finalflight = None
        # bestlength = float('inf')
        # bestfare = float('inf')
        # h = Heap(comp2, arr)
        # while len(h.data)>0:
        #     di, fare, f = h.extract()
        #     if f.end_city == end_city and f.arrival_time <= t2:
        #         if dist[f.flight_no] <= bestlength and fare < bestfare:
        #             bestlength = dist[f.flight_no]
        #             bestfare = fare
        #             finalflight = f
        #     for i in self.adj_by_flight[f.flight_no]:
        #         if i.arrival_time <= t2:
        #             if pre[i.flight_no] == None:
        #                 pre[i.flight_no] = (f, fare)
        #                 dist[i.flight_no] = di + 1
        #                 h.insert((di + 1, i.fare + fare, i))
        #             elif di + 1 <= dist[i.flight_no] and fare < pre[i.flight_no][1]:
        #                 pre[i.flight_no] = (f, fare)
        #                 dist[i.flight_no] = di + 1
        #                 h.insert((di + 1, i.fare + fare, i))
        # if finalflight == None:
        #     return []
        # return self.reconstruct_path(pre, finalflight)
        #



        #code2
        # arrival_time = [None] * self.n
        # dist=[None]*self.n
        # dist[start_city]=0
        # arr_fare = [float('inf')] * self.n
        # arr_fare[start_city] = 0
        # arr_city = [None] * self.n
        # arr_flight = [None] * self.n
        # arrival_time[start_city] = t1 - 20
        # h = Heap(comp2)
        # h.insert((0, 0,start_city)) #(dist. from src, fare,city)
        # while len(h.data) > 0:
        #     d, c, v = h.extract()
        #     for i in self.adj[v]:
        #         if i.departure_time >= arrival_time[v] + 20:
        #             if dist[i.end_city]==None:
        #                 dist[i.end_city]=d+1
        #                 arr_flight[i.end_city] = i
        #                 arr_city[i.end_city] = i.start_city
        #                 arrival_time[i.end_city] = i.arrival_time
        #                 arr_fare[i.end_city] = arr_fare[i.start_city] + i.fare
        #                 h.insert((dist[i.end_city],arr_fare[i.end_city], i.end_city))
        #             elif dist[i.end_city]>=d+1 and arr_fare[i.end_city]>c+i.fare:
        #                 dist[i.end_city] = d + 1
        #                 arr_flight[i.end_city] = i
        #                 arr_city[i.end_city] = i.start_city
        #                 arrival_time[i.end_city] = i.arrival_time
        #                 arr_fare[i.end_city] = arr_fare[i.start_city] + i.fare
        #                 h.insert((dist[i.end_city], arr_fare[i.end_city], i.end_city))
        #
        # if arr_city[end_city] == None or arrival_time[end_city] > t2:
        #     return []
        #
        # v = arr_city[end_city]
        # ans = [arr_flight[end_city]]
        # while v != start_city:
        #     ans.append(arr_flight[v])
        #     v = arr_city[v]
        # ans.reverse()
        # return ans
