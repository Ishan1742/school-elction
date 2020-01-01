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


