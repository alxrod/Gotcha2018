//
//  LoginViewController.swift
//  Gotcha 2018
//
//  Created by Ben Botvinick on 10/25/18.
//  Copyright © 2018 Ben Botvinick. All rights reserved.
//

import UIKit
import Firebase
import FirebaseAuth
import GoogleSignIn

class LoginViewController: UIViewController, GIDSignInUIDelegate {

    override func viewDidLoad() {
        super.viewDidLoad()
        
        GIDSignIn.sharedInstance().uiDelegate = self
    }
    
}
