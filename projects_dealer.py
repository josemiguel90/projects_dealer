import random


class Project:
    def __init__(self, number, title):
        self.__number = number
        self.__title = title

    @property
    def number(self):
        return self.__number

    @property
    def title(self):
        return self.__title

    def __str__(self):
        return f'{self.number}. {self.title}'


class Student:
    def __init__(self, number, name):
        self.__number = number
        self.__name = name

    @property
    def number(self):
        return self.__number

    @property
    def name(self):
        return self.__name

    def __str__(self):
        return f'*** {self.name}'


students = []   # list to store students
projects = []   # list to store projects
initial_distribution = []   # list to store initial distribution of projects


def read_file(filename, list_name, class_name, str_name):
    """ Read data from file and store it in the given list as objects of the specified class """
    br = open(filename, 'r', encoding='UTF8')   # open file in read mode
    for line in br.readlines():   # iterate over file lines
        items = line.split('-')   # split line by -
        if class_name is None:
            list_name.append((int(items[0].strip()), items[1].strip()))   # add tuple (initial distribution)
        else:
            list_name.append(class_name(int(items[0].strip()), items[1].strip()))   # add object of the specified class
    br.close()
    print(f'Load finished -> {len(list_name)} {str_name}')   # show log


def load_data(base_dir=None):
    """ Load data from files in the given base directory"""
    base_dir = base_dir + '/' if base_dir is not None else ''
    read_file(f'{base_dir}students.txt', students, Student, 'students')   # load students
    read_file(f'{base_dir}projects.txt', projects, Project, 'projects')   # load projects
    read_file(f'{base_dir}initial_distribution.txt', initial_distribution, None, 'distributions')   # load initial distribution


def distribute(team_size, base_dir=None):
    """ Distribute projects among students with specified team size """
    if len(students) / team_size > len(projects):   # validate amount of projects for students
        raise Exception(f'Insufficient projects for teams of {team_size} members')
    base_dir = base_dir + '/' if base_dir is not None else ''
    bw = open(f'{base_dir}distribution.txt', 'w', encoding='UTF8')   # create distribution file
    log = open(f'{base_dir}log.txt', 'w', encoding='UTF8')   # create log file
    rnd = random.Random()

    distribution_cont = 0
    selected_students = [False for _ in range(len(students))]   # list to store selected students
    selected_projects = [False for _ in range(len(projects))]   # list to store selected projects

    ### check initial distribution ###
    for project, members in initial_distribution:
        ind_project = None
        for i in range(len(projects)):   # find index of current project
            if projects[i].number == project:
                ind_project = i
                break
        if ind_project is None:   # validate that project exists
            raise Exception(f'Project {project} does not exist.')
        if selected_projects[ind_project]:   # validate that project is not selected
            raise Exception(f'Project {project} already selected.')
        members = [int(x.strip()) for x in members.split(',')]   # parse members of the current project
        if len(members) > team_size:   # validate amount of members
            raise Exception(f'Error in initial distribution for project {project}.')
        ind_members = []
        for mem in members:   # for each member
            ind_stu = None
            for i in range(len(students)):   # find index of current member
                if students[i].number == mem:
                    ind_stu = i
                    break
            if ind_stu is None:   # validate that student exists
                raise Exception(f'Student {mem} does not exist.')
            if selected_students[ind_stu]:   # validate that student is not selected
                raise Exception(f'Student {mem} already selected.')
            for i in ind_members:   # validate that student is not multiple times in the same project
                if i == ind_stu:
                    raise Exception(f'Student {mem} duplicated in the same project.')
            ind_members.append(ind_stu)   # assign student to project
            distribution_cont += 1

        selected_projects[ind_project] = True   # mark project as selected
        bw.write(f'{projects[ind_project]}\n')   # write project on distribution file
        log.write(f'Selecting project index... {ind_project}:valid\n')   # write project index in log file
        for i in range(len(ind_members)):   # for each member of the project
            log.write(f'Selecting team member {str(i + 1)} index... {ind_members[i]}:valid\n')   # write student index in log file
            selected_students[ind_members[i]] = True   # mark student as selected
            bw.write(f'{students[ind_members[i]]}\n')   # write student on distribution file
        bw.write('\n')   # write end-of-line
        log.write('\n')   # write end-of-line

    ### distribute projects ###
    while distribution_cont < len(students):
        log.write('Generating project index... ')   # write message in log file
        p = rnd.randrange(0, len(projects))   # generate random index of the project
        while selected_projects[p]:   # check if project is selected
            log.write(f'{p}:invalid | ')   # write message in log file
            p = rnd.randrange(0, len(projects))   # regenerate random index of the project
        log.write(f'{p}:valid\n')   # write message in log file

        team_members = [-1 for _ in range(team_size)]   # list to store index of team members
        m = 0   # amount of assigned members
        while m < team_size and distribution_cont < len(students):
            log.write(f'Generating team member {str(m + 1)} index... ')   # write message in log file
            while True:
                team_members[m] = rnd.randrange(0, len(students))   # generate random index of the student
                while selected_students[team_members[m]]:   # check if student is selected
                    log.write(f'{team_members[m]}:invalid | ')   # write message in log file
                    team_members[m] = rnd.randrange(0, len(students))   # regenerate random index of the student
                valid = True
                for ind in range(m):   # check if student is not member of the team
                    if team_members[ind] == team_members[m]:
                        log.write(f'{team_members[m]}:invalid | ')   # write message in log file
                        valid = False
                        break
                if valid:
                    break
            log.write(f'{team_members[m]}:valid\n')   # write message in log file
            distribution_cont += 1
            m += 1

        selected_projects[p] = True   # mark project as selected
        bw.write(f'{projects[p]}\n')   # write project on distribution file 

        for t in team_members:   # for each member of the project
            if t == -1:   # check invalid index for incomplete teams (last team)
                break
            selected_students[t] = True   # mark student as selected
            bw.write(f'{students[t]}\n')   # write student on distribution file
        bw.write('\n')   # write end-of-line
        log.write('\n')   # write end-of-line
    bw.close()   # close distribution file
    print('Distribution finished')
    log.close()   # close log file
    print('Log saved')


team_size = 2
base_dir = 'testcase'
load_data(base_dir)
distribute(team_size, base_dir)
