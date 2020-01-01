import pytest
import requests
import string 
import random

SERVER_URL = 'http://localhost:8000/'

def test_signup_login():
    school = {
        'name': 'foo',
        'email': 'bar',
        'password': 'foobar'
    }

    res = requests.post(SERVER_URL + 'signup', json=school)
    
    assert res.status_code == 200

    data = res.json()

    assert data['success'] == True
    assert data['data']['id'] > 0 
    assert data['data']['name'] == school['name']
    assert data['data']['email'] == school['email']
    assert data['data']['password'] == school['password']


    # login success
    school = {
        'email': 'bar',
        'password': 'foobar'
    }

    res = requests.post(SERVER_URL + 'login', json=school)

    assert res.status_code == 200

    data = res.json()

    assert data['success'] == True
    assert data['message']
    assert data['data']

    # login email wrong
    school = {
        'email': 'foo',
        'password': 'foobar'
    }

    res = requests.post(SERVER_URL + 'login', json=school)

    assert res.status_code == 200

    data = res.json()

    assert data['success'] == False
    assert data['message']
    assert data.get('data') == None

    # login password wrong
    school = {
        'email': 'bar',
        'password': 'bar'
    }

    res = requests.post(SERVER_URL + 'login', json=school)

    assert res.status_code == 200

    data = res.json()

    assert data['success'] == False
    assert data['message']
    assert data.get('data') == None

def login():
    school = {
        'email': 'bar',
        'password': 'foobar'
    }

    res = requests.post(SERVER_URL + 'login', json=school)
    data = res.json()

    headers = {
        'Authorization' : 'Bearer {}'.format(data['data'])
    }
    return headers

def test_profile():
    head = login()

    # correct authorization
    res = requests.get(SERVER_URL + 'profile', headers=head)
    assert res.status_code == 200
    data = res.json()
    assert data['success'] == True
    assert data['message']
    assert data['data']['id'] > 0
    assert data['data']['name']
    assert data['data']['email']
    assert data['data']['password']

    # wrong authorization
    res = requests.get(SERVER_URL + 'profile', headers={'Authorization' : 'Bearer apifjpa1q34'})
    assert res.status_code == 401

def randomString(stringLength=10):
    # Generate a random string of fixed length
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def insert_classes():

    head = login()

    classes = {
        'name' : randomString(5),
        'boys' : random.randint(1, 100),
        'girls' : random.randint(1, 100),
    }

    res = requests.post(SERVER_URL + 'classes', headers=head , json=classes)
    data = res.json()
    class_data = data['data']
    return class_data

def test_insert_classes():
    classes = {
        'name' : 'foo',
        'boys' : 24,
        'girls' : 38
    }

    head = login()

    # correct class insertion
    res = requests.post(SERVER_URL + 'classes', headers=head , json=classes)
    assert res.status_code == 200
    data = res.json()
    assert data['success'] == True
    assert data['message']
    assert data['data']['id'] > 0
    assert data['data']['school_id'] > 0
    assert data['data']['name'] == classes['name']
    assert data['data']['boys'] == classes['boys']
    assert data['data']['girls'] == classes['girls']

    # wrong authorization
    res = requests.post(SERVER_URL + 'classes', headers={'Authorization' : 'Bearer apifjpa1q34'}, json=classes)
    assert res.status_code == 401

    # post already existing class
    res = requests.post(SERVER_URL + 'classes', headers=head , json=classes)
    assert res.status_code == 200
    data_repeat = res.json()
    assert data_repeat['data']['id'] != data['data']['id']

def test_put_classes():
    class_data = insert_classes()

    classes = {
        'name' : 'bar',
        'boys' : 41,
        'girls' : 56
    }

    head = login()

    # correct class insertion
    res = requests.put(SERVER_URL + 'classes/{}'.format(class_data['id']), headers=head , json=classes)
    assert res.status_code == 200
    data = res.json()
    assert data['success'] == True
    assert data['message']
    assert data['data']['id'] == class_data['id']
    assert data['data']['school_id'] == class_data['school_id']
    assert data['data']['name'] == classes['name']
    assert data['data']['boys'] == classes['boys']
    assert data['data']['girls'] == classes['girls']

    # wrong authorization
    res = requests.put(SERVER_URL + 'classes/{}'.format(class_data['id']), headers={'Authorization' : 'Bearer apifjpa1q34'}, json=classes)
    assert res.status_code == 401

    # wrong class_id
    head = login()
    res = requests.put(SERVER_URL + 'classes/{}'.format(1234), headers=head, json=classes)
    assert res.status_code == 200
    data = res.json()
    assert data['success'] == False 

def test_delete_classes():
    head = login()
    class_data = insert_classes()
    res = requests.delete(SERVER_URL + 'classes/{}'.format(class_data['id']), headers=head)
    assert res.status_code == 200
    data = res.json()
    assert data['success'] == True
    assert data['data']['id'] == class_data['id']
    assert data['data']['school_id'] == class_data['school_id']
    assert data['data']['name'] == class_data['name']
    assert data['data']['boys'] == class_data['boys']
    assert data['data']['girls'] == class_data['girls']

    # wrong authorization
    class_data = insert_classes()
    res = requests.delete(SERVER_URL + 'classes/{}'.format(class_data['id']), headers={'Authorization' : 'Bearer apifjpa1q34'})
    assert res.status_code == 401

    # wrong class_id
    head = login()
    res = requests.delete(SERVER_URL + 'classes/{}'.format(1234), headers=head)
    assert res.status_code == 200
    data = res.json()
    assert data['success'] == False


def test_get_classes():
    head = login()

    # correct class fetch
    res = requests.get(SERVER_URL + 'classes', headers=head)
    assert res.status_code == 200
    data = res.json()
    assert data['success'] == True
    assert data['message']
    assert data.get('data') != None
    if len(data['data']) > 0:
        assert data['data'][0]['id']
        assert data['data'][0]['school_id']
        assert data['data'][0]['name']
        assert data['data'][0]['boys']
        assert data['data'][0]['girls']

    # wrong authorization
    res = requests.get(SERVER_URL + 'classes', headers={'Authorization' : 'Bearer apifjpa1q34'})
    assert res.status_code == 401

def insert_elections():

    head = login()

    elections = {
        'name' : randomString(5),
        'presidential' : False,
        'genders' : random.randint(1, 3),
    }

    res = requests.post(SERVER_URL + 'elections', headers=head , json=elections)
    data = res.json()
    election_data = data['data']
    return election_data

def test_insert_elections():
    elections = {
        'name' : 'foo',
        'presidential' : False,
        'genders' : 2,
    }

    head = login()

    # correct election insertion
    res = requests.post(SERVER_URL + 'elections', headers=head , json=elections)
    assert res.status_code == 200
    data = res.json()
    assert data['success'] == True
    assert data['message']
    assert data['data']['id'] > 0
    assert data['data']['school_id'] > 0
    assert data['data']['name'] == elections['name']
    assert data['data']['presidential'] == elections['presidential']
    assert data['data']['genders'] == elections['genders']

    # wrong authorization
    res = requests.post(SERVER_URL + 'elections', headers={'Authorization' : 'Bearer apifjpa1q34'}, json=elections)
    assert res.status_code == 401

    # post already existing election
    res = requests.post(SERVER_URL + 'elections', headers=head , json=elections)
    assert res.status_code == 200
    data_repeat = res.json()
    assert data_repeat['data']['id'] != data['data']['id']

def test_put_elections():
    election_data = insert_elections()

    elections = {
        'name' : 'bar',
        'presidential' : True,
        'genders' : 2,
    }

    head = login()

    # correct elections insertion
    res = requests.put(SERVER_URL + 'elections/{}'.format(election_data['id']), headers=head , json=elections)
    assert res.status_code == 200
    data = res.json()
    assert data['success'] == True
    assert data['message']
    assert data['data']['id'] == election_data['id']
    assert data['data']['school_id'] == election_data['school_id']
    assert data['data']['name'] == elections['name']
    assert data['data']['presidential'] == elections['presidential']
    assert data['data']['genders'] == elections['genders']

    # wrong authorization
    res = requests.put(SERVER_URL + 'elections/{}'.format(election_data['id']), headers={'Authorization' : 'Bearer apifjpa1q34'}, json=elections)
    assert res.status_code == 401

    # wrong class_id
    head = login()
    res = requests.put(SERVER_URL + 'elections/{}'.format(1234), headers=head, json=elections)
    assert res.status_code == 200
    data = res.json()
    assert data['success'] == False 

def test_delete_elections():
    head = login()
    election_data = insert_elections()
    res = requests.delete(SERVER_URL + 'elections/{}'.format(election_data['id']), headers=head)
    assert res.status_code == 200
    data = res.json()
    assert data['success'] == True
    assert data['data']['id'] == election_data['id']
    assert data['data']['school_id'] == election_data['school_id']
    assert data['data']['name'] == election_data['name']
    assert data['data']['presidential'] == election_data['presidential']
    assert data['data']['genders'] == election_data['genders']

    # wrong authorization
    election_data = insert_elections()
    res = requests.delete(SERVER_URL + 'elections/{}'.format(election_data['id']), headers={'Authorization' : 'Bearer apifjpa1q34'})
    assert res.status_code == 401

    # wrong election_id
    head = login()
    res = requests.delete(SERVER_URL + 'elections/{}'.format(1234), headers=head)
    assert res.status_code == 200
    data = res.json()
    assert data['success'] == False


def test_get_elections():
    head = login()

    # correct election fetch
    res = requests.get(SERVER_URL + 'elections', headers=head)
    assert res.status_code == 200
    data = res.json()
    assert data['success'] == True
    assert data['message']
    assert data.get('data') != None
    if len(data['data']) > 0:
        assert data['data'][0]['id']
        assert data['data'][0]['school_id']
        assert data['data'][0]['name']
        assert data['data'][0]['presidential'] == False or data['data'][0]['presidential'] == True
        assert data['data'][0]['genders']
    

    # wrong authorization
    res = requests.get(SERVER_URL + 'elections', headers={'Authorization' : 'Bearer apifjpa1q34'})
    assert res.status_code == 401

def test_get_voter():

    student = {
        'student_num' : 4,
        'class_id' : 1,
        'gender' : 2,
    }    

    res = requests.post(SERVER_URL + 'voter/get', json=student)
    assert res.status_code == 200
    data = res.json()
    assert data['success'] == True
    assert data['message']
    assert data.get('data') != None
    if len(data['data']) >0:
        assert data['data'][0]['id']
        assert data['data'][0]['election_name']
        assert data['data'][0]['name']
        assert data['data'][0]['symbol']

def test_cast_voter():

    vote = {
        'student_num' : 4,
        'class_id' : 1,
        'vote_candidate_ids' : [1, 2, 3, 4],
    }

    res = requests.post(SERVER_URL + 'voter/cast', json=vote)
    assert res.status_code == 200
    data = res.json()
    assert data['success'] == True 
    assert data['message']