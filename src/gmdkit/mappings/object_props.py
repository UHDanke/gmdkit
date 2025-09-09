class prop_id:
    id = 1
    x = 2
    y = 3
    flip_x = 4
    flip_y = 5
    rotation = 6
    old_color_id = 19
    editor_l1 = 20
    color_1 = 21
    color_2 = 22
    z_layer = 24
    z_order = 25
    old_scale = 32
    group_parent = 34
    hsv_enabled_1 = 41
    hsv_enabled_2 = 42
    hsv_1 = 43
    hsv_2 = 44
    groups = 57
    editor_l2 = 61
    dont_fade = 64
    dont_enter = 67
    no_glow = 96
    high_detail = 103
    linked_group = 108
    no_effects = 116
    no_touch = 121
    scale_x = 128
    scale_y = 129
    skew_x = 131
    skew_y = 132
    passable = 134
    hide = 135
    nonstick_x = 136
    ice_block = 137
    color_1_index = 155
    color_2_index = 156
    grip_slope = 193
    target_player_2 = 200
    parent_groups = 274
    area_parent = 279
    nonstick_y = 289
    enter_channel = 343
    scale_stick = 356
    disable_grid_snap = 370
    no_audio_scale = 372
    material = 446
    extra_sticky = 495
    dont_boost_y = 496
    single_color_type = 497
    no_particle = 507
    dont_boost_x = 509
    extended_collision = 511

    class animated:
        randomize_start = 106
        animation_speed = 107
        use_speed = 122
        animate_on_trigger = 123
        delayed_loop = 126
        animate_active_only = 214
        single_frame = 462
        offset_anim = 592

        class explosion:
            disable_shine = 127

    class item_label:
        item_id = 80
        seconds_only = 389
        special_id = 390
        alignment = 391
        time_counter = 466
        kerning = 488

    class level:
        audio_track = 'kA1'
        input_2p = 'kA10'
        flip_gravity = 'kA11'
        color_3_blending = 'kA12'
        song_offset = 'kA13'
        song_guidelines = 'kA14'
        song_fade_in = 'kA15'
        song_fade_out = 'kA16'
        ground_line = 'kA17'
        font = 'kA18'
        gamemode = 'kA2'
        reverse_mode = 'kA20'
        platformer_mode = 'kA22'
        _kA23 = 'kA23'
        _kA24 = 'kA24'
        middleground = 'kA25'
        allow_multi_rotate = 'kA27'
        mirror_mode = 'kA28'
        rotate_mode = 'kA29'
        mini_mode = 'kA3'
        enable_player_squeeze = 'kA31'
        fix_gravity_bug = 'kA32'
        fix_negative_scale = 'kA33'
        fix_robot_jump = 'kA34'
        player_spawn = 'kA36'
        dynamic_height = 'kA37'
        sort_groups = 'kA38'
        fix_radius_collision = 'kA39'
        speed = 'kA4'
        enable_2_2_changes = 'kA40'
        allow_static_object_rotate = 'kA41'
        reverse_sync = 'kA42'
        disable_time_point_penalty = 'kA43'
        decrease_boost_slide = 'kA45'
        song_dont_reset = 'kA46'
        object_2_blending = 'kA5'
        background = 'kA6'
        ground = 'kA7'
        dual_mode = 'kA8'
        is_start_pos = 'kA9'
        colors = 'kS38'
        color_page = 'kS39'

        class color_1_7:

            class background:
                red = 'kS1'
                player_color = 'kS16'
                green = 'kS2'
                blue = 'kS3'

            class ground:
                player_color = 'kS17'
                red = 'kS4'
                green = 'kS5'
                blue = 'kS6'

            class line:
                player_color = 'kS18'
                red = 'kS7'
                green = 'kS8'
                blue = 'kS9'

            class object:
                red = 'kS10'
                green = 'kS11'
                blue = 'kS12'
                player_color = 'kS19'

            class object_2:
                red = 'kS13'
                green = 'kS14'
                blue = 'kS15'
                player_color = 'kS20'

        class color_1_9:
            background = 'kS29'
            ground = 'kS30'
            line = 'kS31'
            object = 'kS32'
            color_1 = 'kS33'
            color_2 = 'kS34'
            color_3 = 'kS35'
            color_4 = 'kS36'
            line_3d = 'kS37'

    class particle:
        data = 145
        use_obj_color = 146
        uniform_obj_color = 147
        quick_start = 211

    class saw:
        rotation_speed = 97
        disable_rotation = 98

    class start_pos:
        target_order = 'kA19'
        reverse_mode = 'kA20'
        disable = 'kA21'
        platformer_mode = 'kA22'
        _kA23 = 'kA23'
        _kA24 = 'kA24'
        _kA25 = 'kA25'
        target_channel = 'kA26'
        allow_multi_rotate = 'kA27'
        mirror_mode = 'kA28'
        rotate_mode = 'kA29'
        enable_player_squeeze = 'kA31'
        fix_gravity_bug = 'kA32'
        fix_negative_scale = 'kA33'
        fix_robot_jump = 'kA34'
        reset_camera = 'kA35'
        _kA36 = 'kA36'
        dynamic_height = 'kA37'
        sort_groups = 'kA38'
        fix_radius_collision = 'kA39'
        enable_2_2_changes = 'kA40'
        allow_static_object_rotate = 'kA41'
        reverse_sync = 'kA42'
        disable_time_point_penalty = 'kA43'
        _kA44 = 'kA44'
        decrease_boost_slide = 'kA45'
        song_dont_reset = 'kA46'

    class template:
        reference_only = 157

    class text:
        data = 31
        kerning = 488

    class timewarp:
        mod = 120

    class trigger:
        touch_triggered = 11
        editor_preview = 13
        interactible = 36
        spawn_triggered = 62
        multi_trigger = 87
        multi_activate = 99
        order = 115
        reverse = 117
        channel = 170
        ignore_gparent = 280
        ignore_linked = 281
        single_ptouch = 284
        center_effect = 369
        disable_multi_activate = 444
        control_id = 534

        class adv_follow:
            target_id = 51
            follow_id = 71
            player_1 = 138
            player_2 = 200
            corner = 201
            delay = 292
            delay_rand = 293
            max_speed = 298
            max_speed_rand = 299
            start_speed = 300
            start_speed_rand = 301
            target_dir = 305
            x_only = 306
            y_only = 307
            max_range = 308
            max_range_rand = 309
            _310 = 310
            _311 = 311
            _312 = 312
            _313 = 313
            _314 = 314
            _315 = 315
            steer = 316
            steer_rand = 317
            steer_low = 318
            steer_low_rand = 319
            steer_high = 320
            steer_high_rand = 321
            speed_range_low = 322
            speed_range_low_rand = 323
            speed_range_high = 324
            speed_range_high_rand = 325
            break_force = 326
            break_force_rand = 327
            break_angle = 328
            break_angle_rand = 329
            break_steer = 330
            break_steer_rand = 331
            break_steer_speed_limit = 332
            break_steer_speed_limit_rand = 333
            acceleration = 334
            acceleration_rand = 335
            ignore_disabled = 336
            steer_low_check = 337
            steer_high_check = 338
            rotate_dir = 339
            rot_offset = 340
            near_accel = 357
            near_accel_rand = 358
            near_dist = 359
            near_dist_rand = 360
            easing = 361
            easing_rand = 362
            rot_easing = 363
            rot_deadzone = 364
            priority = 365
            max_range_ref = 366
            mode = 367
            friction = 558
            friction_rand = 559
            start_speed_ref = 560
            near_friction = 561
            near_friction_rand = 562
            start_dir = 563
            start_dir_rand = 564
            start_dir_ref = 565
            exclusive = 571
            init = 572

        class adv_random:
            _56 = 56
            targets = 152

        class alpha:
            duration = 10
            opacity = 35
            group_id = 51

        class animate:
            target_id = 51
            animation_id = 76

        class animate_keyframe:
            target_id = 51
            parent_id = 71
            animation_id = 76
            time_mod = 520
            pos_x_mod = 521
            rotation_mod = 522
            scale_x_mod = 523
            pos_y_mod = 545
            scale_y_mod = 546

        class arrow:
            dir_y = 166
            dir_x = 167
            edit_velocity = 169
            change_channel = 171
            channel_only = 172
            target_channel = 173
            instant_offset = 368
            velocity_mod_x = 582
            velocity_mod_y = 583
            override_velocity = 584
            dont_slide = 585

        class bg_speed:
            x_mod = 143
            y_mod = 144

        class bpm:
            duration = 10
            bpm = 498
            speed = 499
            disable = 500
            bpb = 501

        class camera_edge:
            target_id = 51
            direction = 164

        class camera_guide:
            offset_x = 28
            offset_y = 29
            zoom = 371
            preview_opacity = 506

        class camera_mode:
            free_mode = 111
            edit_settings = 112
            easing = 113
            padding = 114

        class change_bg:
            id = 533

        class change_g:
            id = 533

        class change_mg:
            id = 533

        class checkpoint:
            spawn_id = 51
            target_pos = 71
            player_pos = 138
            respawn_id = 448

        class collectible:
            group_id = 51
            sub_count = 78
            item_id = 80
            pickup_item = 381
            toggle_trigger = 382
            points = 383
            particle = 440
            no_anim = 463

            class coin:
                coin_id = 12

        class collision:
            _10 = 10
            target_id = 51
            activate_group = 56
            block_a = 80
            exit = 93
            block_b = 95
            player_1 = 138
            player_2 = 200
            between_players = 201

        class collision_block:
            block_id = 80
            dynamic = 94

        class color:
            red = 7
            green = 8
            blue = 9
            duration = 10
            tint_ground = 14
            player_1 = 15
            player_2 = 16
            blending = 17
            channel = 23
            opacity = 35
            hsv = 49
            copy_id = 50
            copy_opacity = 60
            disable_legacy_hsv = 210

        class count:
            target_id = 51
            activate_group = 56
            count = 77
            item_id = 80
            multi_activate = 104

        class dash:
            speed = 586
            collide = 587
            end_boost = 588
            stop_slide = 589
            max_duration = 590

        class edit_adv_follow:
            target_id = 51
            follow_id = 71
            player_1 = 138
            player_2 = 200
            corner = 201
            _292 = 292
            _293 = 293
            _298 = 298
            _299 = 299
            speed = 300
            speed_rand = 301
            _305 = 305
            x_only = 306
            y_only = 307
            _308 = 308
            _309 = 309
            _310 = 310
            _311 = 311
            _312 = 312
            _313 = 313
            _314 = 314
            _315 = 315
            _316 = 316
            _317 = 317
            _318 = 318
            _319 = 319
            _320 = 320
            _321 = 321
            _322 = 322
            _323 = 323
            _324 = 324
            _325 = 325
            _326 = 326
            _327 = 327
            _328 = 328
            _329 = 329
            _330 = 330
            _331 = 331
            _332 = 332
            _333 = 333
            _334 = 334
            _335 = 335
            _336 = 336
            _337 = 337
            _338 = 338
            _339 = 339
            _340 = 340
            _357 = 357
            _358 = 358
            _359 = 359
            _360 = 360
            _361 = 361
            _362 = 362
            _363 = 363
            _364 = 364
            _365 = 365
            _366 = 366
            _367 = 367
            use_control_id = 535
            _558 = 558
            _559 = 559
            speed_ref = 560
            _561 = 561
            _562 = 562
            dir = 563
            dir_rand = 564
            dir_ref = 565
            mod_x = 566
            mod_x_rand = 567
            mod_y = 568
            mod_y_rand = 569
            redirect_dir = 570
            _571 = 571
            _572 = 572

        class effect:
            duration = 10
            hsv = 49
            target_id = 51
            main_only = 65
            detail_only = 66
            center_id = 71
            _138 = 138
            _200 = 200
            _201 = 201
            enter_only = 217
            move_dist = 218
            move_dist_rand = 219
            offset = 220
            offset_rand = 221
            length = 222
            length_rand = 223
            _224 = 224
            effect_id = 225
            move_angle = 231
            move_angle_rand = 232
            scale_x = 233
            scale_x_rand = 234
            scale_y = 235
            scale_y_rand = 236
            move_x = 237
            move_x_rand = 238
            move_y = 239
            move_y_rand = 240
            xy_mode = 241
            easing = 242
            easing_rate = 243
            easing_2 = 248
            easing_rate_2 = 249
            offset_y = 252
            offset_y_rand = 253
            tint_channel = 260
            ease_out = 261
            direction = 262
            mod_front = 263
            mod_back = 264
            tint = 265
            rotate = 270
            rotate_rand = 271
            to_opacity = 275
            inwards = 276
            enable_hsv = 278
            deadzone = 282
            mirrored = 283
            _285 = 285
            from_opacity = 286
            relative = 287
            rfade = 288
            priority = 341
            enter_channel = 344
            use_effect_id = 355
            special_center = 538
            deap = 539

        class end:
            spawn_id = 51
            target_pos = 71
            no_effects = 460
            no_sfx = 461
            instant = 487

        class end_wall:
            group_id = 51
            lock_y = 59
            reverse = 118

        class enter_preset:
            enter_only = 217
            enter_channel = 344

        class event:
            spawn_id = 51
            events = 430
            _431 = 431
            extra_id_1 = 447
            extra_id_2 = 525

        class follow:
            duration = 10
            target_id = 51
            follow_target = 71
            mod_x = 72
            mod_y = 73

        class follow_player_y:
            duration = 10
            target_id = 51
            speed = 90
            delay = 91
            offset = 92
            max_speed = 105

        class force_block:
            value = 149
            value_min = 526
            value_max = 527
            relative = 528
            range = 529
            force_id = 530

        class gamemode_portal:
            free_mode = 111
            edit_settings = 112
            easing = 113
            padding = 114

        class gameplay_offset:
            offset_x = 28
            offset_y = 29
            dont_zoom_x = 58
            dont_zoom_y = 59

        class gradient:
            blending = 174
            layer = 202
            u = 203
            bl = 203
            d = 204
            br = 204
            l = 205
            tl = 205
            r = 206
            tr = 206
            vertex_mode = 207
            disable = 208
            gradient_id = 209
            preview_opacity = 456
            disable_all = 508

        class gravity:
            player_1 = 138
            value = 148
            player_2 = 200
            player_touch = 201

        class instant_collision:
            true_id = 51
            false_id = 71
            block_a = 80
            block_b = 95
            player_1 = 138
            player_2 = 200
            between_players = 201

        class instant_count:
            target_id = 51
            activate_group = 56
            count = 77
            item_id = 80
            mode = 88

        class item_compare:
            true_id = 51
            false_id = 71
            item_id_1 = 80
            item_id_2 = 95
            item_type_1 = 476
            item_type_2 = 477
            mod_1 = 479
            item_op_1 = 480
            item_op_2 = 481
            item_op_3 = 482
            mod_2 = 483
            tolerance = 484
            round_op_1 = 485
            round_op_2 = 486
            sign_op_1 = 578
            sign_op_2 = 579

        class item_edit:
            target_item_id = 51
            item_id_1 = 80
            item_id_2 = 95
            item_type_1 = 476
            item_type_2 = 477
            item_type_3 = 478
            mod = 479
            item_op_1 = 480
            item_op_2 = 481
            item_op_3 = 482
            round_op_1 = 485
            round_op_2 = 486
            sign_op_1 = 578
            sign_op_2 = 579

        class item_persist:
            item_id = 80
            set_persistent = 491
            target_all = 492
            reset = 493
            timer = 494

        class keyframe:
            duration = 10
            easing = 30
            group_id = 51
            spawn_id = 71
            ease_rate = 85
            key_id = 373
            index = 374
            ref_only = 375
            close_loop = 376
            prox = 377
            curve = 378
            time_mode = 379
            preview_art = 380
            auto_layer = 459
            line_opacity = 524
            spin_direction = 536
            full_rotations = 537
            spawn_delay = 557

        class link_visible:
            group_id = 51

        class mg_edit:
            duration = 10
            offset_y = 29
            easing = 30
            ease_rate = 85

        class mg_speed:
            x_mod = 143
            y_mod = 144

        class move:
            duration = 10
            move_x = 28
            move_y = 29
            easing = 30
            target_id = 51
            lock_player_x = 58
            lock_player_y = 59
            target_pos = 71
            ease_rate = 85
            target_mode = 100
            target_axis = 101
            player_1 = 138
            lock_camera_x = 141
            lock_camera_y = 142
            follow_x_mod = 143
            follow_y_mod = 144
            player_2 = 200
            use_small_step = 393
            direction_mode = 394
            target_center_id = 395
            target_distance = 396
            dynamic_mode = 397
            _516 = 516
            _517 = 517
            _518 = 518
            _519 = 519
            silent = 544

        class object_control:
            target_id = 51

        class offset_camera:
            offset_x = 28
            offset_y = 29
            easing = 30
            ease_rate = 85
            axis = 101

        class offset_gameplay:
            axis = 101

        class on_death:
            group_id = 51
            activate_group = 56

        class options:
            streak_additive = 159
            unlink_dual_gravity = 160
            hide_ground = 161
            hide_p1 = 162
            hide_p2 = 163
            disable_p1_controls = 165
            hide_mg = 195
            disable_controls_p1 = 199
            hide_attempts = 532
            edit_respawn_time = 573
            respawn_time = 574
            audio_on_death = 575
            disable_death_sfx = 576
            boost_slide = 593

        class orb_saw:
            rotation_speed = 97

            class disable:
                rotation = 98

        class pickup:
            count = 77
            item_id = 80
            mode = 88
            override = 139
            mod = 449

        class player_control:
            _58 = 58
            _59 = 59
            player_1 = 138
            _141 = 141
            player_2 = 200
            stop_jump = 540
            stop_move = 541
            stop_rotation = 542
            stop_slide = 543

        class pulse:
            red = 7
            green = 8
            blue = 9
            fade_in = 45
            hold = 46
            fade_out = 47
            use_hsv = 48
            hsv = 49
            copy_id = 50
            target_id = 51
            target_type = 52
            main_only = 65
            detail_only = 66
            exclusive = 86
            disable_static_hsv = 210

        class random:
            chance = 10
            true_id = 51
            false_id = 71

        class reset:
            group_id = 51

        class rotate:
            duration = 10
            easing = 30
            target_id = 51
            degrees = 68
            full = 69
            lock_rotation = 70
            rotate_target = 71
            ease_rate = 85
            aim_mode = 100
            player_1 = 138
            player_2 = 200
            follow_mode = 394
            dynamic_mode = 397
            aim_target = 401
            aim_offset = 402
            aim_easing = 403
            min_x_id = 516
            min_y_id = 517
            max_x_id = 518
            max_y_id = 519

        class rotate_camera:
            duration = 10
            easing = 30
            degrees = 68
            add = 70
            ease_rate = 85
            snap_360 = 394

        class scale:
            duration = 10
            easing = 30
            target_id = 51
            center_id = 71
            ease_rate = 85
            only_move = 133
            scale_by_x = 150
            scale_by_y = 151
            div_by_x = 153
            div_by_y = 154
            relative_rotation = 452
            relative_scale = 577

        class sequence:
            sequence = 435
            mode = 436
            min_interval = 437
            reset_time = 438
            reset_type = 439
            unique_remap = 505

        class sfx:
            duration = 10
            group_id_1 = 51
            group_id_2 = 71
            player_1 = 138
            player_2 = 200
            sfx_id = 392
            speed = 404
            pitch = 405
            volume = 406
            use_reverb = 407
            start = 408
            fade_in = 409
            end = 410
            fade_out = 411
            fft = 412
            loop = 413
            unique = 415
            unique_id = 416
            stop_loop = 417
            change_volume = 418
            change_speed = 419
            override = 420
            vol_near = 421
            vol_med = 422
            vol_far = 423
            dist_1 = 424
            dist_2 = 425
            dist_3 = 426
            camera = 428
            pre_load = 433
            min_int = 434
            group = 455
            group_id = 457
            direction = 458
            ignore_volume = 489
            sfx_duration = 490
            reverb = 502
            override_reverb = 503
            _595 = 595
            speed_rand = 596
            pitch_rand = 597
            volume_rand = 598
            pitch_steps = 599

        class shader:
            fade_time = 10
            easing = 30
            shockwave_center_id = 51
            shockline_center_id = 51
            lens_circle_center_id = 51
            radial_blur_center_id = 51
            motion_blur_center_id = 51
            bulge_center_id = 51
            pinch_center_id = 51
            gray_scale_tint_channel = 51
            lens_circle_tint_channel = 71
            radial_blur_ref_channel = 71
            motion_blur_ref_channel = 71
            ease_rate = 85
            shockwave_player_1 = 138
            shockline_player_1 = 138
            lens_circle_player_1 = 138
            radial_blur_player_1 = 138
            motion_blur_player_1 = 138
            bulge_player_1 = 138
            pinch_player_1 = 138
            shockwave_speed = 175
            shockline_speed = 175
            glitch_speed = 175
            chromatic_glitch_speed = 175
            edit_color_CB = 175
            shockwave_strength = 176
            shockline_strength = 176
            glitch_strength = 176
            chromatic_glitch_strength = 176
            lens_circle_strength = 176
            radial_blur_intensity = 176
            motion_blur_intensity = 176
            bulge_bulge = 176
            gray_scale_target = 176
            sepia_target = 176
            invert_color_target = 176
            hue_degrees = 176
            edit_color_CR = 176
            shockwave_time_offset = 177
            shockline_time_offset = 177
            shockwave_wave_width = 179
            shockline_wave_width = 179
            glitch_slice_height = 179
            chromatic_glitch_line_thickness = 179
            lens_circle_size = 179
            radial_blur_size = 179
            pinch_modifier = 179
            invert_color_R = 179
            edit_color_BR = 179
            shockwave_thickness = 180
            shockline_thickness = 180
            chromatic_target_x = 180
            chromatic_glitch_rgb_offset = 180
            pixelate_target_x = 180
            motion_blur_target_x = 180
            bulge_radius = 180
            pinch_target_x = 180
            invert_color_G = 180
            edit_color_BG = 180
            split_screen_target_x = 180
            shockwave_fade_in = 181
            shockline_fade_in = 181
            glitch_max_col_x_offset = 181
            lens_circle_fade = 181
            radial_blur_fade = 181
            motion_blur_fade = 181
            shockwave_fade_out = 182
            shockline_fade_out = 182
            glitch_max_col_y_offset = 182
            shockwave_inner = 183
            shockwave_invert = 184
            shockline_invert = 184
            shockline_flip = 185
            shockline_rotate = 186
            shockline_dual = 187
            shader_opt_ignore_player_particles = 188
            shockwave_target = 188
            shockline_target = 188
            chromatic_use_x = 188
            pixelate_use_x = 188
            radial_blur_target = 188
            motion_blur_use_x = 188
            bulge_target = 188
            pinch_target = 188
            gray_scale_use_tint = 188
            invert_color_edit_rgb = 188
            split_screen_use_x = 188
            chromatic_target_y = 189
            chromatic_glitch_segment_h = 189
            pixelate_target_y = 189
            motion_blur_target_y = 189
            invert_color_B = 189
            edit_color_BB = 189
            split_screen_target_y = 189
            shockwave_follow = 190
            shockline_follow = 190
            chromatic_use_y = 190
            pixelate_use_y = 190
            motion_blur_use_y = 190
            pinch_use_x = 190
            gray_scale_use_lum = 190
            invert_color_tween_rgb = 190
            split_screen_use_y = 190
            shockwave_outer = 191
            glitch_max_slice_x_offset = 191
            chromatic_glitch_line_strength = 191
            motion_blur_follow_ease = 191
            edit_color_CG = 191
            shader_opt_disable_all = 192
            chromatic_glitch_disable = 192
            chromatic_glitch_relative_pos = 194
            pixelate_snap_grid = 194
            motion_blur_dual_dir = 194
            pinch_use_y = 194
            invert_color_clamp_rgb = 194
            shader_opt_layer_min = 196
            shader_opt_layer_max = 197
            shockwave_player_2 = 200
            shockline_player_2 = 200
            lens_circle_player_2 = 200
            radial_blur_player_2 = 200
            motion_blur_player_2 = 200
            bulge_player_2 = 200
            pinch_player_2 = 200
            motion_blur_center = 201
            shockwave_screen_offset_x = 290
            shockline_screen_offset = 290
            lens_circle_screen_offset_x = 290
            radial_blur_screen_offset_x = 290
            bulge_screen_offset_x = 290
            pinch_screen_offset_x = 290
            shockwave_screen_offset_y = 291
            lens_circle_screen_offset_y = 291
            radial_blur_screen_offset_y = 291
            bulge_screen_offset_y = 291
            pinch_screen_offset_y = 291
            shockwave_max_size = 512
            shockline_max_size = 512
            pinch_radius = 512
            shockwave_animate = 513
            shockline_animate = 513
            shockwave_relative = 514
            shockline_relative = 514
            glitch_relative = 514
            chromatic_relative = 514
            chromatic_glitch_relative = 514
            pixelate_relative = 514
            lens_circle_relative = 514
            motion_blur_relative = 514
            bulge_relative = 514
            relative = 514
            pixelate_hard_edges = 515
            radial_blur_empty_only = 515
            motion_blur_empty_only = 515
            disable_preview = 531

        class shake:
            duration = 10
            strength = 75
            interval = 84

        class song:
            duration = 10
            group_id_1 = 51
            group_id_2 = 71
            player_1 = 138
            player_2 = 200
            song_id = 392
            prep = 399
            load_prep = 400
            speed = 404
            _405 = 405
            volume = 406
            _407 = 407
            start = 408
            fade_in = 409
            end = 410
            fade_out = 411
            _412 = 412
            loop = 413
            _415 = 415
            _416 = 416
            stop_loop = 417
            change_volume = 418
            change_speed = 419
            _420 = 420
            vol_near = 421
            vol_med = 422
            fol_var = 423
            dist_1 = 424
            dist_2 = 425
            dist_3 = 426
            camera = 428
            channel = 432
            _433 = 433
            _434 = 434
            _455 = 455
            _457 = 457
            direction = 458
            _489 = 489
            _490 = 490
            _502 = 502
            _503 = 503
            dont_reset = 595
            _596 = 596
            _597 = 597
            _598 = 598
            _599 = 599

        class spawn:
            group_id = 51
            duration = 63
            disable_preview = 102
            ordered = 441
            remaps = 442
            delay_rand = 556
            reset_remap = 581

        class spawn_particle:
            particle_group = 51
            position_group = 71
            offset_x = 547
            offset_y = 548
            offvar_x = 549
            offvar_y = 550
            match_rot = 551
            rotation = 552
            rotation_rand = 553
            scale = 554
            scale_rand = 555

        class state_block:
            state_on = 51
            state_off = 71

        class static:
            axis = 101

        class static_camera:
            easing = 30
            target_id = 71
            ease_rate = 85
            exit = 110
            follow_group = 212
            follow_easing = 213
            smooth_velocity = 453
            velocity_mod = 454
            exit_instant = 465

        class stop:
            target_id = 51
            use_control_id = 535
            mode = 580

        class teleport:
            target_id = 51
            smooth_ease = 55
            use_force = 345
            force = 346
            redirect_force = 347
            force_min = 348
            force_max = 349
            force_mod = 350
            keep_offset = 351
            ignore_x = 352
            ignore_y = 353
            gravity = 354
            additive_force = 443
            instant_camera = 464
            snap_ground = 510
            redirect_dash = 591

            class exit_portal:
                _350 = 350

            class portal:
                distance = 54

        class time:
            item_id = 80
            start_time = 467
            dont_override = 468
            ignore_timewarp = 469
            mod = 470
            start_paused = 471
            target_id = 473
            stop = 474

        class time_control:
            item_id = 80
            stop = 472

        class time_event:
            item_id = 80
            target_id = 473
            multi_activate = 475

        class toggle:
            group_id = 51
            activate_group = 56

        class toggle_block:
            group_id = 51
            activate_group = 56
            claim_touch = 445
            spawn_only = 504

        class touch:
            group_id = 51
            hold_mode = 81
            toggle_mode = 82
            dual_mode = 89
            only_player = 198

        class ui:
            group_id = 51
            ui_target = 71
            ref_x = 385
            ref_y = 386
            relative_x = 387
            relative_y = 388

        class zoom_camera:
            duration = 10
            easing = 30
            ease_rate = 85
            zoom = 371
