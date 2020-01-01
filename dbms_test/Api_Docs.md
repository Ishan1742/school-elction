-- Authentication

POST /signup
    Request: {
        name: String
        email: String
        password: String
    }
    Response: {
        success: bool,
        message: String,
        data: {
            id: i32,
            name: String
            email: String
            password: String
        }
    }



POST /login
    Request: {
        email: String
        password: String
    }
    Response: {
        success: bool,
        message: String,
        data: String        # token
    }


-- Data Administration (These routes require JWT)

GET /profile
    Response: {
        success: bool,
        message: String,
        data: {
            id: i32,
            name: String,
            email: String,
            password: String,
        }
    }

---- Classes

GET /classes
    Response: {
        success: bool,
        message: String,
        data: [{
            id: i32,
            school_id: i32,
            name: String,
            boys: i32,
            girls: i32,
        }]
    }


POST /classes
    Request: {
        name: String,
        boys: i32,
        girls: i32
    }
    Response: {
        success: bool,
        message: String,
        data: {
            id: i32,
            school_id: i32,
            name: String,
            boys: i32,
            girls: i32,
        }
    }

PUT /classes/id
    Request: {
        name: String,
        boys: i32,
        girls: i32
    }
    Response: {
        success: bool,
        message: String,
        data: {
            id: i32,
            school_id: i32,
            name: String,
            boys: i32,
            girls: i32,
        }
    }

DELETE /classes/id
    Response: {
        success: bool,
        message: String,
        data: {
            id: i32,
            school_id: i32,
            name: String,
            boys: i32,
            girls: i32,
        }
    }

---- Elections

GET /elections
    Response: {
        success: bool,
        message: String,
        data: [{
            id: i32,
            school_id: i32,
            name: String,
            presidential: bool,
            genders: i32,
        }]
    }


POST /elections
    Request: {
        name: String,
        presidential: bool,
        genders: i32
    }
    Response: {
        success: bool,
        message: String,
        data: {
            id: i32,
            school_id: i32,
            name: String,
            presidential: bool,
            genders: i32,
        }
    }

PUT /elections/id
    Request: {
        name: String,
        presidential: bool,
        genders: i32
    }
    Response: {
        success: bool,
        message: String,
        data: {
            id: i32,
            school_id: i32,
            name: String,
            presidential: bool,
            genders: i32,
        }
    }

DELETE /elections/id
    Response: {
        success: bool,
        message: String,
        data: {
            id: i32,
            school_id: i32,
            name: String,
            presidential: bool,
            genders: i32,
        }
    }


---- Candidates

GET /candidates
    Response: {
        success: bool,
        message: String,
        data: [{
            id: i32,
            name: String,
            school_id: i32,
            election_id: i32,
            class_id: i32,
            gender: i32,
            symbol: String,
        }]
    }


POST /candidates
    Request: {
        name: String,
        school_id: i32,
        election_id: i32,
        class_id: i32,
        gender: i32,
        symbol: String,
    }
    Response: {
        success: bool,
        message: String,
        data: {
            id: i32,
            name: String,
            school_id: i32,
            election_id: i32,
            class_id: i32,
            gender: i32,
            symbol: String,
        }
    }

PUT /candidates/id
    Request: {
        name: String,
        school_id: i32,
        election_id: i32,
        class_id: i32,
        gender: i32,
        symbol: String,
    }
    Response: {
        success: bool,
        message: String,
        data: {
            id: i32,
            name: String,
            school_id: i32,
            election_id: i32,
            class_id: i32,
            gender: i32,
            symbol: String,
        }
    }

DELETE /candidates/id
    Response: {
        success: bool,
        message: String,
        data: {
            id: i32,
            name: String,
            school_id: i32,
            election_id: i32,
            class_id: i32,
            gender: i32,
            symbol: String,
        }
    }


-- Voting (Does not require JWT)

POST /voter/get
    Request: {
        student_num: i32,
        class_id: i32,
        gender: i32
    }
    Response: {
        sucess: bool,
        message: String,
        data: [{            # List of all candidates he/she can cast votes for
            id: i32,
            election_name: String,
            name: String,
            symbol: String
        }]
    }

POST /voter/cast
    Request: {
        student_num: i32,
        class_id: i32,
        vote_candidate_ids: [i32]
    }
    Response: {
        success: bool,
        message: String
    }
