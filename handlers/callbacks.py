elif data == "apply_coach":
        from handlers.coach import apply_coach
        await apply_coach(update, context)

    elif data == "coach_dashboard":
        from handlers.coach import coach_dashboard
        await coach_dashboard(update, context)

    elif data == "coach_show_link":
        from handlers.coach import show_coach_link
        await show_coach_link(update, context)

    elif data == "coach_leaderboard":
        from handlers.coach import show_leaderboard
        await show_leaderboard(update, context)

    elif data.startswith("coach_approve_"):
        if not is_master_admin(query.from_user.id):
            await query.edit_message_text("Unauthorized.")
            return
        coach_id = int(data.split("_")[2])
        cursor.execute(
            "INSERT INTO coaches (chat_id, approved_by, is_active) VALUES (%s, %s, TRUE) "
            "ON CONFLICT (chat_id) DO UPDATE SET is_active=TRUE, approved_by=%s",
            (coach_id, query.from_user.id, query.from_user.id)
        )
        conn.commit()
        await context.bot.send_message(coach_id, "Congratulations! You are now an official FortuneX Coach!\n\nGo to /menu → Coach Dashboard to get your link.")
        await query.edit_message_text(f"Coach {coach_id} approved successfully!")

    elif data.startswith("coach_reject_"):
        if not is_master_admin(query.from_user.id):
            return
        coach_id = int(data.split("_")[2])
        await context.bot.send_message(coach_id, "Your FortuneX Coach application was not approved at this time.\nYou may reapply later.")
        await query.edit_message_text(f"Application from {coach_id} rejected.")

elif data == "pkg_standard":
        cursor.execute("UPDATE users SET package='Standard' WHERE chat_id=%s", (query.from_user.id,))
        conn.commit()
        await query.edit_message_text(
            "You selected *FortuneX Standard* ₦7,500\n\n"
            "Please make payment to any of the accounts and send screenshot.",
            parse_mode="Markdown"
        )

    elif data == "pkg_pro":
        cursor.execute("UPDATE users SET package='Pro' WHERE chat_id=%s", (query.from_user.id,))
        conn.commit()
        await query.edit_message_text(
            "You selected *FortuneX Pro* ₦14,500\n\n"
            "You get 10× earnings, loan access, and more!\n"
            "Please make payment and send screenshot.",
            parse_mode="Markdown"
        )

    elif data == "package_selector":
        from handlers.start import package_selector
        await package_selector(update, context)
