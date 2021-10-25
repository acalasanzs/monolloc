void Scheduler::RoundRob(queue<PCB> &input) {

	bool differentArrivals = true;
	int timer = 0;
	bool fetched = false; //if a single process in ready queue
	bool removed = false; //if a process completed

	int idleTime = 0;
	vector<int> waitingTimes;
	vector<int> turnAround;
	vector<int> responseTime;


	do {

		while (!input.empty() && input.front().arrivalTime <= timer && !fetched) {
			readyQueue->push(&input.front());
			input.pop();
		}

		if (readyQueue->head && readyQueue->tail && readyQueue->head->next && 
			readyQueue->head->arrivalTime != readyQueue->head->next->arrivalTime && differentArrivals && !removed) {
				readyQueue->head = readyQueue->head->next;
				readyQueue->tail = readyQueue->tail->next;
		}
		else {
			removed = false;
			differentArrivals = true;
		}

		if (readyQueue->head) {
			if (readyQueue->head->burstTime == readyQueue->head->originalBurst) {
				responseTime.push_back(timer - readyQueue->head->arrivalTime);
			}
		}


		for (int i = 0; i < timeQuantum; i++) {
				x.push_back(timer);
				y.push_back(readyQueue->head->pid);
			if (!(readyQueue->head->burstTime > 0)) {
				cout << "Finished process: " << readyQueue->head->pid << endl;
				turnAround.push_back(timer - readyQueue->head->arrivalTime);
				waitingTimes.push_back((timer - readyQueue->head->arrivalTime) - readyQueue->head->originalBurst);
				readyQueue->pop();
				removed = true;
				break;
			}
			else if (readyQueue->head->burstTime > 0) {
				readyQueue->head->burstTime -= 1;
			}
			else {
				cout << "<Time: " << timer << "> Process running: IDLE" << endl;
				timer += 1;
				idleTime++;
			}
			Sleep(1);	
			cout << "<Time: " << timer << "> Process running: " << readyQueue->head->pid << endl;
			timer += 1;
		}
		

		if (readyQueue->head == readyQueue->tail) {
			while (!input.empty() && input.front().arrivalTime <= timer) {
				readyQueue->push(&input.front());
				input.pop();
				fetched = true;
			}
		}
		else
			fetched = false;

		if (readyQueue->head != NULL) {
			if (readyQueue->head->arrivalTime == readyQueue->head->next->arrivalTime && readyQueue->head != readyQueue->head->next) {
				readyQueue->head = readyQueue->head->next;
				readyQueue->tail = readyQueue->tail->next;
				differentArrivals = false;
			}
		}
		else {
			differentArrivals = true;
		}	
		
	} while (readyQueue->head != NULL || !input.empty());

	cout << "CPU Usage: " << (((timer - idleTime) / timer) * 100) << "%" << endl;
	cout << "Average Waiting Time: " << (accumulate(waitingTimes.begin(), waitingTimes.end(), 0) / waitingTimes.size()) << endl;
	cout << "Average Response Time: " << (accumulate(responseTime.begin(), responseTime.end(), 0) / responseTime.size()) << endl;
	cout << "Average Turnaround Time: " << (accumulate(turnAround.begin(), turnAround.end(), 0) / turnAround.size()) << endl;

}