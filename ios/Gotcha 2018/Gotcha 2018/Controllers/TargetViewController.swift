//
//  TargetViewController.swift
//  Gotcha 2018
//
//  Created by Ben Botvinick on 10/25/18.
//  Copyright © 2018 Ben Botvinick. All rights reserved.
//

import UIKit

class TargetViewController: UIViewController {
    @IBOutlet weak var targetLabel: UILabel!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        self.targetLabel.text = "Alex Rodriguez"
        
    }

}
