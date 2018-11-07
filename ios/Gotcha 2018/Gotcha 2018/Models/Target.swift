//
//  Target.swift
//  Gotcha 2018
//
//  Created by Ben Botvinick on 10/27/18.
//  Copyright © 2018 Ben Botvinick. All rights reserved.
//

import Foundation

class Target: Codable {
    
    var id: String
    var name: String
    
    init(id: String, name: String) {
        self.id = id
        self.name = name
    }
    
    private static var _current: Target?
    
    static var current: Target {
        guard let currentTarget = _current else {
            fatalError("Error: current target doesn't exist")
        }
        
        return currentTarget
    }
    
    class func setCurrent(_ target: Target, writeToUserDefaults: Bool = false) {
        if writeToUserDefaults {
            if let data = try? JSONEncoder().encode(target) {
                UserDefaults.standard.set(data, forKey: Constants.UserDefaults.currentTarget)
            }
        }
        
        _current = target
    }
    
    static func getId(email: String) -> String {
        return email.components(separatedBy: "@")[0]
    }
}
