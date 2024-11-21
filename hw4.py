import county_demographics
import sys

from build_data import convert_county
from data import CountyDemographics


def display(county:CountyDemographics):
    print(f"{county.county}, {county.state}")
    print("Population:")
    for i in county.population:
        print("\t{}: {}".format(i, county.population[i]))
    print("Age:")
    for i in county.age:
        print("\t{}: {}".format(i, county.age[i]))

    print("County:")
    print(f"    County: {county.county}")

    print("Education:")
    for i in county.education:
        print("\t{}: {}".format(i, county.education[i]))

    print("Ethnicities:")
    for i in county.ethnicities:
        print("\t{}: {}".format(i, county.ethnicities[i]))

    print("Income:")
    for i in county.income:
        print("\t{}: {}".format(i, county.income[i]))


    print("State:")
    print(f"    State: {county.state}")

def filterstate(datascope, state):
    newscope = []
    for i in datascope:
        if i.state == state:
            newscope.append(i)
    return newscope

def filtergt(datascope, field, num):
    newscope = []
    farray = field.split(".")
    for i in datascope:
        if farray[0] == "Education":
            if i.education[farray[1]] > num:
                newscope.append(i)
        if farray[0] == "Ethnicities":
            if i.ethnicities[farray[1]] > num:
                newscope.append(i)
        if farray[0] == "Income":
            if i.income[farray[1]] > num:
                newscope.append(i)
    return newscope

def filterlt(datascope, field, num):
    farray = field.split(".")

    newscope = []
    for i in datascope:
        if farray[0] == "Education":
            if i.education[farray[1]] < num:
                newscope.append(i)
        if farray[0] == "Ethnicities":
            if i.ethnicities[farray[1]] < num:
                newscope.append(i)
        if farray[0] == "Income":
            if i.income[farray[1]] < num:
                newscope.append(i)
    return newscope

def pop_total(datascope):
    total = 0
    try:
        for i in datascope:
            total += i.population['2014 Population']
        print("2014 population: {}".format(total))
    except KeyError as e:
        print(e)
    return total

def population(datascope, field):
    farray = field.split(".")
    total = 0
    for i in datascope:
        if farray[0] == "Education":
            total += i.population['2014 Population']*i.education[farray[1]]
        if farray[0] == "Ethnicities":
            total += i.population['2014 Population'] * i.ethnicities[farray[1]]
        if farray[0] == "Income":
            total += i.population['2014 Population'] * i.income[farray[1]]
    return total
def percent(datascope, field):
    farray = field.split(".")
    total = 0
    subtotal = 0
    for county in datascope:
        try:
            if farray[0] == "Education":
                total += county.population['2014 Population']
                subtotal += county.population['2014 Population'] * (county.education[farray[1]] / 100)
            elif farray[0] == "Ethnicities":
                total += county.population['2014 Population']
                subtotal += county.population['2014 Population'] * (county.ethnicities[farray[1]] / 100)
            elif farray[0] == "Income":
                total += county.population['2014 Population']
                subtotal += county.population['2014 Population'] * (county.income[farray[1]] / 100)
        except KeyError as e:
            print(f"KeyError for field '{field}' in county {county.county}. Skipping.")
            continue

    if total == 0:
        return 0.0
    return (subtotal / total) * 100


def execute_operation():
    entries = 0
    linenum = 0
    try:
        f = open(str(sys.argv[1]))
        data = open("county_demographics.data")
        counties = [convert_county(county) for county in county_demographics.get_report()]
        datascope = counties
        entries = len(counties)
        print("{} records loaded".format(entries))
        for i in f:
            ops = i.split(":")
            for z in range(len(ops)):
                if "\n" in ops[z]:
                    ops[z] = ops[z][:-1]

            if ops[0] == "display":
                for z in datascope:
                    display(z)
            elif ops[0] == "filter-state":
                datascope = filterstate(datascope, ops[1])
                print("Filter: state == {} ({} entries)".format(ops[1], len(datascope)))
            elif ops[0] == "filter-gt":
                try:
                    datascope = filtergt(datascope, ops[1], float(ops[2]))
                    print("Filter: {} > {} ({} entries)".format(ops[1], ops[2], len(datascope)))
                except:
                    print("One or more arguments invalid.")
            elif ops[0] == "filter-lt":
                try:
                    datascope = filterlt(datascope, ops[1], float(ops[2]))
                    print("Filter: {} < {} ({} entries)".format(ops[1], ops[2], len(datascope)))
                except:
                    print("One or more arguments invalid.")

            elif ops[0] == "population-total":
                pop_total(datascope)

            elif ops[0] == "population":
                print("2014 {} population: {}".format(ops[1], population(datascope, ops[1])))
            elif ops[0] == "percent":
                print("2014 {} percentage: {}".format(ops[1], percent(datascope, ops[1])))
            else:
                    print("Could not read operation. Skipping line.")
            linenum += 1
        f.close()
        data.close()
    except KeyError as e:
        print(e)

if __name__ == "__main__":
    execute_operation()
