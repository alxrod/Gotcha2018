//
//  User.swift
//  Gotcha 2018
//
//  Created by Ben Botvinick on 10/25/18.
//  Copyright © 2018 Ben Botvinick. All rights reserved.
//

import Foundation

class User: Codable {
    
    var id: String? = nil
    var name: String? = nil
    var target: String? = nil
    
    init(id: String?, name: String?, target: String?) {
        self.id = id
        self.name = name
        self.target = target
    }
    
    private static var _current: User?
    
    static var current: User {
        guard let currentUser = _current else {
            fatalError("Error: current user doesn't exist")
        }
        
        return currentUser
    }
    
    class func setCurrent(_ user: User, writeToUserDefaults: Bool = false) {
        if writeToUserDefaults {
            if let data = try? JSONEncoder().encode(user) {
                UserDefaults.standard.set(data, forKey: Constants.UserDefaults.currentUser)
                UserDefaults.standard.set(true, forKey: Constants.UserDefaults.firstTime)
            }
        }
        
        _current = user
    }
}
