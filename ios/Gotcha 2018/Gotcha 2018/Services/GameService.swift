//
//  GameService.swift
//  Gotcha 2018
//
//  Created by Ben Botvinick on 10/25/18.
//  Copyright © 2018 Ben Botvinick. All rights reserved.
//

import Foundation
import Firebase

struct GameService {
    static func getTargetId(userId: String, completion: @escaping (String?) -> Void) {
        let ref = Database.database().reference(withPath: "circle/\(userId)")
        
        ref.observeSingleEvent(of: .value, with: { (snapshot) in
            guard let target = snapshot.value as? String else { return completion(nil) }
            completion(target)
        }) { (error) in
            print(error.localizedDescription)
            completion(nil)
        }
    }
}
