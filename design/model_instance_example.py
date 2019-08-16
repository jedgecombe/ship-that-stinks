def repr2(obj, file_object,level = 1):
    dict = obj.__dict__
    sublevel = level -1
    nextlevel = level + 1
    dict_list = {}
    for key, item in dict.items():
        if (isinstance(item, db_object)):
            dict_list[key] = item
        elif (str(key) == "object_type" or str(key) == "table_name"):
            pass
        else:
            file_object.write(("\t" * level) + "<" + str(key) + ">" + str(item) + "</" + str(key) + ">")
    for key, item in dict_list.items():
        file_object.write("<" + key + ">")
        repr2(item, file_object, nextlevel)
        file_object.write("</" + key + ">")

#Abstract database class enabling CRUD functionality for all children
class db_object:
    def __init__(self):
        self.id = -1
        self.table_name = "not_yet_defined"
        self.object_type = "db_object"
        self.load_status = False

    # Reads an object record from the specified database table
    # Not sure again how this can be done
    def read(self, id):
        pass
        # Maybe for key in self.__dict__ select key from DB where ID = id
        # There's gonna be a library / function for this I've just never done it

    # Writes an object record to the specified database table
    def create(self):
        filestring = self.__dict__['object_type'] + '.xml'
        print "Output: " + filestring
        file_object = open(filestring, 'w')
        file_object.write("<" + self.table_name + ">" )
        repr2(self, file_object)
        file_object.write("</" + self.table_name + ">")
        # repr(self.__dict__, file_object)
        file_object.close()
        self.load_status = True

    # Updates the given record in the specified databse table; this one
    # is likely more difficult to implement
    def update(self):
        print "Updating this record in the database"

    # Deletes the given record from the specified databse table.
    # Can likely be done based on record ID alone
    def delete(self):
        print "Deleting the following record from the database: "
        #repr(self.__dict__)

class session_user(db_object):
    def __init__(self):
        self.is_authenticated = False
        self.is_active = False
        self.is_anonymous = True
        self.email = "Blank email"
        self.password_hash = "Not your business"
    def create(self, email, password):
        self.email = email
        self.password_hash = password + " hashed"
    def authenticate(self, email, password):
        self.email = email
        self.is_authenticated = True
    def get_id():
        pass


# Participant class representing basic attributes for the members
class participant(session_user):
    def __init__(self):
        session_user.__init__(self)
        self.id = 1
        self.table_name = "participants"
        self.object_type = "Participant"
    def create(self, first_name, surname, email, nickname, origination_date):
        self.first_name = first_name
        self.surname = surname
        self.email = email
        self.nickname = nickname
        self.origination_date = origination_date
        db_object.create(self)
    def register_attendance(self, attendee, event):
        this_attendance = attendance()
        this_attendance.create(self, attendee, event)
        return this_attendance

# Attendance class enabling identification of an event attendance
# in reference to the event and the attendee
class attendance(db_object):
    def __init__(self):
        self.id = 1
        self.table_name = "attendance"
        self.object_type = "Attendance"
    def create(self, recording_party, attendee, event):
        self.recording_party = recording_party
        self.attendee = attendee
        self.event = event
        db_object.create(self)

# Extends the pariticpant class and exposes the functionality to register
# attendance, and propose an event
class organiser(participant):
    def __init__(self):
        participant.__init__(self)
        self.object_type = "Organiser"
    def propose_event(self, event, proposal_date, proposal_time):
        this_proposal = event_proposal()
        this_proposal.create(self, event, proposal_date, proposal_time)
        return this_proposal

# CLass representing the response to an event proposal
class proposal_response(db_object):
    def __init__(self):
        self.id = 1
        self.table_name = "proposal_response"
        self.object_type = "Proposal Response"
    def create(self, responding_party, proposal, response, response_date, response_time):
        self.response_date = response_date
        self.response_time = response_time
        self.responding_party = responding_party
        self.proposal = proposal
        self.response = response
        db_object.create(self)

# Extends the participant class and exposes the functionality open to attendees
# to respond to event proposals
class attendee(participant):
    def __init__(self):
        participant.__init__(self)
        self.object_type = "Attendee"
    def respond_to_proposal(self, proposal, response, response_date, response_time):
        this_response = proposal_response()
        this_response.create(self, proposal, response, response_date, response_time)
        return this_response

# Event class enabling identification of basic event attributes
class event(db_object):
    def __init__(self):
        self.id = 1
        self.table_name = "event"
        self.object_type = "Event"
    def create(self, event_name, event_date, event_time, event_location):
        self.event_name = event_name
        self.event_date = event_date
        self.event_time = event_time
        self.event_location = event_location
        db_object.create(self)


# Class enabling the representation of a location
class location(db_object):
    def __init__(self):
        self.table_name = "location"
        self.object_type = "Location"
        self.id = 1
    def create(self, lat, long, name):
        self.lat = lat
        self.long = long
        self.name = name
        db_object.create(self)

# Class representing the proposal for an event encompassing the event
# and the organising participant who proposes it
class event_proposal(db_object):
    def __init__(self):
        self.object_type = "Event Proposal"
        self.table_name = "event_proposal"
        self.id = 1
    def create(self, organiser, event, proposal_date, proposal_time):
        self.proposal_date = "01.01.1970"
        self.proposal_time = "20:00"
        self.event = event
        self.organiser = organiser
        db_object.create(self)

# Set of example steps which demonstrate the creation of organisers,
# locations, events, proposals, attendees, and event responses

marv = organiser()
marv.create("James", "Marvin", "j_marvin@mail.com", "Marv", "01.01.1970")

marv_and_dyls = location()
marv_and_dyls.create(-00.00,-00.00, "Marv and Dyl's")

pizza_at_marvs = event()
pizza_at_marvs.create("Pizza at Marv's", "01.01.1980", "21:00", marv_and_dyls)

proposal = marv.propose_event(pizza_at_marvs, "01.01.1990", "22:00")

jalfrezi = attendee()
jalfrezi.create("James", "Edgecombe", "j.edgecombe@hello-sailor.com", "Jal","01.01.2000")

jalfrezi.respond_to_proposal(proposal, "Accepted", "01.01.2010", "23:00")

dyl = participant()
dyl.create("Dylan", "Drake", "dylandrake@me.com", "Dyl", "01.01.2020")


noted_attendance = dyl.register_attendance(jalfrezi, pizza_at_marvs)

print noted_attendance.attendee.nickname + " went to the event '" + noted_attendance.event.event_name + "' on " + noted_attendance.event.event_date + ". "
print "The event was at " + noted_attendance.event.event_location.name + ", and his presence was noted by " + noted_attendance.recording_party.nickname
