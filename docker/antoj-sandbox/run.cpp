#include <cstdio>
#include <cstdlib>
#include <iostream>
#include <string>
#include <vector>

#include <pthread.h>
#include <pwd.h>
#include <signal.h>
#include <string.h>
#include <sys/resource.h>
#include <sys/timeb.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

using namespace std;

const uid_t SANDBOX_UID = 1111;
const gid_t SANDBOX_GID = 1111;

struct {
	int time_limit; // ms.
	int mem_limit;	// kb.
	int disk_limit; // mb.
	string input_file;
	string output_file;
	string stderr_file;

	string cmd;
	vector<string> cmd_argv;
} RunConfig;

pid_t child_pid;

void print_help(char *name) {
	// TODO: complete the help.
	printf("Usage: %s TIME_LIMIT(ms) MEM_LIMIT(kb) INPUT_FILE OUTPUT_FILE STDERR_FILE CMD [CMD_ARGS...]\n", name);
}

void load_config(int argc, char *argv[]) {
	RunConfig.time_limit = atoi(argv[1]);
	RunConfig.mem_limit = atoi(argv[2]);
	// RunConfig.disk_limit = atoi(argv[3]);
	RunConfig.input_file = string(argv[3]);
	RunConfig.output_file = string(argv[4]);
	RunConfig.stderr_file = string(argv[5]);
	RunConfig.cmd = string(argv[6]);
	RunConfig.cmd_argv.push_back(RunConfig.cmd);

	for (int i = 7; i < argc; i++)
		RunConfig.cmd_argv.push_back(string(argv[i]));
}

void print_config_int(const char *hints, int metric) {
	printf("%s", hints);
	if (metric)
		printf("%d\n", metric);
	else
		printf("unlimited\n");
}

void print_config_str(const char *hints, string str) {
	printf("%s", hints);
	if (str.length())
		printf("%s\n", str.c_str());
	else
		printf("undefined\n");
}

void print_config() {
	print_config_int("Time Limit (ms): ", RunConfig.time_limit);
	print_config_int("Memory Limit (kb): ", RunConfig.mem_limit);
	print_config_int("Disk Limit (mb): ", RunConfig.disk_limit);
	print_config_str("Input File: ", RunConfig.input_file);
	print_config_str("Output File: ", RunConfig.output_file);
	print_config_str("Stderr File: ", RunConfig.stderr_file);
	string cmd;
	for (int i = 0; i < RunConfig.cmd_argv.size(); i++)
		cmd += RunConfig.cmd_argv[i] + " ";
	print_config_str("Command: ", cmd);
}

bool is_root() {
	return getuid() == 0;
}

long long get_system_time() {
	struct timeb t;
	ftime(&t);
	return 1000 * t.time + t.millitm;
}

void *watcher_thread(void *arg) {
	sleep(RunConfig.time_limit / 1000 + 2);
	kill(child_pid, SIGXCPU);
	return arg; // Avoid 'parameter set but not used' warning
}

int main(int argc, char *argv[]) {
	if (!is_root()) {
		printf("The sandbox must be run with root privilege!");
		return -1;
	}
	if (argc < 7) {
		print_help(argv[0]);
		return -1;
	}

	chdir("/sandbox");

	if (chown(".", SANDBOX_UID, SANDBOX_GID) == -1) {
		perror("chown failed");
		return -1;
	}

	load_config(argc, argv);
	// print_config();

	child_pid = fork();

	if (child_pid > 0) {
		if (RunConfig.time_limit) {
			pthread_t thread_id;
			pthread_create(&thread_id, NULL, &watcher_thread, NULL);
		}
		long long start = get_system_time();

		FILE *fresult = fopen("ReSultS.TxT", "w");

		struct rusage usage;
		int status, sig = 0;
		if (wait4(child_pid, &status, 0, &usage) == -1) {
			fprintf(fresult, "Runtime Error\nwait4() = -1\n0\n0\n");
			return 0;
		}
		long long end = get_system_time();
		// int time_usage = (usage.ru_utime.tv_sec * 1000000ll + usage.ru_utime.tv_usec) / 1000;
		int time_usage = end - start;
		int mem_usage = usage.ru_maxrss;

		if (!WIFEXITED(status)) {
			// Signaled
			sig = WTERMSIG(status);
		}

		if (WIFEXITED(status) && WEXITSTATUS(status) != 0) {
			fprintf(fresult, "Runtime Error\nstatus = %d WIFEXITED - WEXITSTATUS() = %d\n", status, WEXITSTATUS(status));
		} else if (sig == SIGSEGV || sig == SIGABRT) {
			// Segment fault or exception
			fprintf(fresult, "Runtime Error\nstatus = %d SIG = %d\n", status, sig);
		} else if (sig == SIGXCPU || (RunConfig.time_limit && time_usage > RunConfig.time_limit)) {
			fprintf(fresult, "Time Limit Exceeded\nWEXITSTATUS() = %d, WTERMSIG() = %d (%s)\n", WEXITSTATUS(status), sig, strsignal(sig));
		} else if (sig == SIGXFSZ) {
			fprintf(fresult, "Output Limit Exceeded\nWEXITSTATUS() = %d, WTERMSIG() = %d (%s)\n", WEXITSTATUS(status), sig, strsignal(sig));
		} else if (RunConfig.mem_limit && mem_usage > RunConfig.mem_limit) {
			fprintf(fresult, "Memory Limit Exceeded\nWEXITSTATUS() = %d, WTERMSIG() = %d (%s)\n", WEXITSTATUS(status), sig, strsignal(sig));
		} /*else if (WIFEXITED(status)){
			fprintf(fresult, "Accepted\nWIFEXITED - WEXITSTATUS() = %d\n", WEXITSTATUS(status));
		} */
		else {
			fprintf(fresult, "Accepted\nWIFEXITED - WEXITSTATUS() = %d\n", WEXITSTATUS(status));
			// fprintf(fresult, "Runtime Error\nWEXITSTATUS() = %d, WTERMSIG() = %d (%s)\n", WEXITSTATUS(status), sig, strsignal(sig));
		}

		fprintf(fresult, "%d\n%d\n", time_usage, mem_usage);
		fclose(fresult);
	} else {
		if (RunConfig.time_limit) {
			/*
			struct rlimit lim;
			lim.rlim_cur = (RunConfig.time_limit + 2000) / 1000;
			lim.rlim_max = (RunConfig.time_limit + 2000) / 1000;
			setrlimit(RLIMIT_CPU, &lim);
			*/
		}

		if (RunConfig.mem_limit) {
			/*
			struct rlimit lim;
			lim.rlim_cur = (RunConfig.mem_limit + 20 * 1024) * 1024;
			lim.rlim_max = (RunConfig.mem_limit + 20 * 1024) * 1024;
			setrlimit(RLIMIT_AS, &lim);
			setrlimit(RLIMIT_STACK, &lim);
			*/
		}

		/*
		{
			struct rlimit lim;
			lim.rlim_cur = 256 * 1000 * 1024;
			lim.rlim_max = 256 * 1000 * 1024;
			setrlimit(RLIMIT_FSIZE, &lim);
		}*/

		{
			struct rlimit lim;
			lim.rlim_cur = 2000;
			lim.rlim_max = 2000;
			setrlimit(RLIMIT_NPROC, &lim);
		}

		setuid(SANDBOX_UID);
		setgid(SANDBOX_GID);

		if (RunConfig.input_file.length())
			freopen(RunConfig.input_file.c_str(), "r", stdin);
		else
			freopen("/dev/null", "r", stdin);
		if (RunConfig.output_file.length()) {
			freopen(RunConfig.output_file.c_str(), "w", stdout);
		} else {
			freopen("/dev/null", "w", stdout);
		}
		if (RunConfig.stderr_file.length()) {
			freopen(RunConfig.stderr_file.c_str(), "w", stderr);
		} else {
			freopen("/dev/null", "w", stderr);
		}

		char *ch_argv[64] = {};
		for (int i = 6; i < argc; i++) {
			ch_argv[i - 6] = argv[i];
		}
		execvp(RunConfig.cmd.c_str(), ch_argv);
	}
}
