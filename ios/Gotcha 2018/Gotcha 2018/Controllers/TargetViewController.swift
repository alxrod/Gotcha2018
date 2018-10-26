//
//  TargetViewController.swift
//  Gotcha 2018
//
//  Created by Ben Botvinick on 10/25/18.
//  Copyright © 2018 Ben Botvinick. All rights reserved.
//

import UIKit

class TargetViewController: UIViewController {

    override func viewDidLoad() {
        super.viewDidLoad()
        
        GameService.getTargetId(userId: User.current.id) { target in
            print(target!)
        }
    }


}

