import datetime
import random
import time
import os

class Player:
    def __init__(self, name, number, position):
        self.name = name
        self.number = number
        self.position = position
        self.level = 1
        self.experience = 0
        self.skill_stats = {
            'Speed': 50,
            'Shooting': 50,
            'Dribbling': 50,
            'Passing': 50,
            'Defending': 50,
            'Goalkeeping': 50,
            'Positioning': 50,   
            'Vision': 50         
        }
        self.skill_level = sum(self.skill_stats.values()) / len(self.skill_stats)
        self.money = 1000
        self.energy = 100
        self.fame = 0
        self.morale = 75
        self.injuries = []
        self.form = 50
        self.red_card = False
        self.yellow_cards = 0
        self.goals = 0
        self.assists = 0

    def train(self, attribute):
        if self.energy >= 10:
            improvement = random.randint(1, 3)
            self.skill_stats[attribute] = min(100, self.skill_stats[attribute] + improvement)
            self.energy -= 10
            self.experience += 5
            self.morale += 2
            self.form = min(100, self.form + random.randint(1, 5))
            return improvement
        return 0

    def rest(self):
        self.energy = min(100, self.energy + 20)
        self.morale += 5
        self.form = max(0, self.form - random.randint(1, 3))
        print("You have rested and regained some energy and morale.")

    def update_after_match(self, performance_score):
        self.energy = max(0, self.energy - random.randint(30, 50))
        self.experience += performance_score
        self.form = max(0, min(100, self.form + random.randint(-10, 20)))
        self.morale = max(0, min(100, self.morale + random.randint(-10, 15)))

class Club:
    def __init__(self, name, country, skill_level, reputation):
        self.name = name
        self.country = country
        self.skill_level = skill_level
        self.reputation = reputation
        self.league_position = random.randint(1, 20)
        self.fans = random.randint(10000, 1000000)
        self.stadium = f"{name} Stadium"
        self.stadium_capacity = random.randint(20000, 80000)

class SoccerCareer:
    def __init__(self):
        self.player = self.create_player()
        self.current_date = datetime.date(2024, 1, 1)
        self.current_club = None
        self.available_clubs = self.generate_clubs()
        self.events = self.initialize_events()
        self.running = True
        self.season = 1
        self.days_until_match = random.randint(2, 6)
        self.has_trained_this_week = False
        self.media_interaction_chance = 0.1
        self.achievements = []
        self.league_table = self.initialize_league_table()

    def create_player(self):
        name = input("Enter your player's name: ")
        number = self.get_input("Choose your jersey number (1-99): ", range(1, 100))
        position = self.choose_position()
        return Player(name, number, position)

    def choose_position(self):
        positions = ['Goalkeeper', 'Defender', 'Midfielder', 'Forward']
        print("Select your position:")
        for i, position in enumerate(positions, start=1):
            print(f"{i}. {position}")
        choice = self.get_input("Your choice: ", range(1, len(positions) + 1))
        return positions[choice - 1]

    def generate_clubs(self):
        countries = ["Brazil", "Germany", "Italy", "Spain", "England", "France", "Argentina", "Netherlands"]
        clubs = []
        for country in countries:
            for i in range(3):
                name = f"{country} {'United' if i == 0 else 'City' if i == 1 else 'Athletic'} FC"
                skill_level = random.randint(60, 90)
                reputation = random.choice(["Local", "National", "Continental", "Global"])
                clubs.append(Club(name, country, skill_level, reputation))
        return clubs

    def initialize_events(self):
        return [
            {"date": datetime.date(2024, 3, 1), "event": "first_match", "message": "Your first major league match is approaching!"},
            {"date": datetime.date(2024, 7, 1), "event": "transfer_window", "message": "The summer transfer window has opened."},
            {"date": datetime.date(2024, 11, 1), "event": "sponsorship_deal", "message": "A major sportswear brand is interested in sponsoring you."},
            {"date": datetime.date(2025, 1, 1), "event": "new_year", "message": "Happy New Year! Time to set new career goals."},
            {"date": datetime.date(2025, 5, 15), "event": "international_callup", "message": "You've received your first international call-up!"}
        ]

    def initialize_league_table(self):
        return {club.name: {'Points': 0, 'GF': 0, 'GA': 0} for club in self.available_clubs}

    def start_game(self):
        self.clear_screen()
        print("\n🌟 Welcome to Soccer Superstar: The Ultimate Career Simulation! 🌟")
        print("Your journey from rookie to legend begins now.\n")
        self.choose_initial_club()
        while self.running:
            self.process_week()

    def choose_initial_club(self):
        print(f"{self.player.name}, your talent has caught the eye of several clubs!")
        available_clubs = random.sample(self.available_clubs, 5)
        print("\nClubs interested in signing you:")
        for i, club in enumerate(available_clubs, 1):
            print(f"{i}. {club.name} ({club.country}) - Skill Level: {club.skill_level}, Reputation: {club.reputation}")

        choice = self.get_input("\nSelect the club you want to join (1-5): ", range(1, 6))
        self.current_club = available_clubs[int(choice) - 1]
        print(f"\nCongratulations! You've signed your first professional contract with {self.current_club.name}.")
        print(f"The fans are eager to see you in action at {self.current_club.stadium}!")
        self.player.money += 5000
        print("You've received a $5,000 signing bonus!")


    def process_week(self):
        while self.days_until_match > 0:
            self.check_for_events()
            self.display_status()
            self.weekly_choices()
            
            if self.has_trained_this_week:
                self.days_until_match = 0 
            else:
                self.days_until_match -= 1 
        if random.random() < self.media_interaction_chance:
            self.media_interaction()
            self.media_interaction_chance = 0 

        self.play_match()

        if self.media_interaction_chance > 0:
            if random.random() < self.media_interaction_chance:
                self.media_interaction()

        self.days_until_match = random.randint(2, 6)
        self.has_trained_this_week = False
        self.media_interaction_chance = 0.1
        
        self.advance_week()
        self.check_season_end()

    def check_for_events(self):
        for event in self.events:
            if event["date"] == self.current_date:
                print(f"\n🚨 BREAKING NEWS: {event['message']}")
                if event["event"] == "transfer_window":
                    self.handle_transfer_window()
                elif event["event"] == "sponsorship_deal":
                    self.handle_sponsorship_deal()
                elif event["event"] == "international_callup":
                    self.handle_international_callup()

    def handle_transfer_window(self):
        if self.get_input("Do you want to explore transfer options? (y/n): ", ['y', 'n']) == 'y':
            new_clubs = random.sample([club for club in self.available_clubs if club != self.current_club], 3)
            print("\nTransfer offers:")
            for i, club in enumerate(new_clubs, 1):
                offer = max(10000, self.player.level * 5000 + random.randint(-1000, 1000))
                print(f"{i}. {club.name} ({club.country}) - Offer: ${offer:,}")
            choice = self.get_input("Select an offer (0 to stay at current club): ", range(0, 4))
            if choice != '0':
                self.current_club = new_clubs[int(choice) - 1]
                self.player.money += int(offer)
                print(f"Transfer complete! You now play for {self.current_club.name}.")
                print(f"Transfer fee received: ${offer:,}")
                self.achievements.append(f"Transferred to {self.current_club.name}")

    def handle_sponsorship_deal(self):
        deal_value = self.player.level * 10000 + random.randint(5000, 20000)
        if self.get_input(f"Accept a ${deal_value:,} sponsorship deal? (y/n): ", ['y', 'n']) == 'y':
            self.player.money += deal_value
            self.player.fame += 20
            print(f"Congratulations! You've signed a lucrative sponsorship deal worth ${deal_value:,}.")
            self.achievements.append("Signed major sponsorship deal")

    def handle_international_callup(self):
        print("You've been called up to represent your national team!")
        performance = random.randint(1, 100)
        if performance > 70:
            print("You had an outstanding international debut!")
            self.player.fame += 30
            self.player.morale += 20
            self.achievements.append("Successful international debut")
        else:
            print("You played in your first international match. There's room for improvement.")
            self.player.fame += 10
            self.player.morale += 5
    
    def calculate_performance_impact(self, outcome):
        if "GOAL" in outcome or "well done" in outcome:
            return random.randint(8, 15)
        elif "Oh no" in outcome or "intercepts" in outcome or "mistimed" in outcome:
            return random.randint(-10, -5)
        elif "saved" in outcome or "deflects" in outcome:
            return random.randint(-5, 5)
        else:
            return random.randint(-3, 5)


    def display_status(self):
        self.clear_screen()
        print(f"\n--- {self.player.name}'s Career Status ---")
        print(f"Date: {self.current_date} | Season: {self.season}")
        print(f"Club: {self.current_club.name}")
        print(f"Level: {self.player.level} (Exp: {self.player.experience}/{self.player.level * 100})")
        print(f"Energy: {self.player.energy} | Morale: {self.player.morale} | Form: {self.player.form}")
        print(f"Money: ${self.player.money:,} | Fame: {self.player.fame}")
        print(f"Days until next match: {self.days_until_match}")

    def weekly_choices(self):
        while True:
            print(f"\nThere are {self.days_until_match} days before the match. What would you like to do?")
            
            if not self.has_trained_this_week:
                print("1. Intense Training")
                print("2. Light Training")
                print("3. Rest")
            
            print("4. View Detailed Stats")
            print("5. View Achievements")
            print("6. View League Table")

            valid_choices = [4, 5, 6] if self.has_trained_this_week else list(range(1, 7))
            choice = self.get_input("Your choice: ", valid_choices)

            if choice in [1, 2, 3] and not self.has_trained_this_week:
                if choice == 1:
                    self.intense_training()
                elif choice == 2:
                    self.light_training()
                else:
                    self.player.rest()
                self.has_trained_this_week = True
                break
            elif choice == 4:
                self.view_stats()
            elif choice == 5:
                self.view_achievements()
            elif choice == 6:
                self.view_league_table()

            if self.has_trained_this_week:
                break
            else:
                input("\nPress Enter to continue...")

    def intense_training(self):
        print("You have chosen intense training.")
        if self.player.energy >= 20:
            skill_to_train = random.choice(list(self.player.skill_stats.keys()))
            improvement = random.randint(3, 5)
            self.player.skill_stats[skill_to_train] = min(100, self.player.skill_stats[skill_to_train] + improvement)
            self.player.energy -= 20
            self.player.experience += 10
            self.player.form = min(100, self.player.form + random.randint(1, 5))
            print(f"Your {skill_to_train} has improved by {improvement} points.")
            if random.random() < 0.1:
                self.player.injuries.append("Minor Injury")
                print("You have sustained a minor injury during intense training.")
        else:
            print("Not enough energy for intense training. Consider resting.")

    def light_training(self):
        print("You have chosen light training.")
        if self.player.energy >= 10:
            skills_to_train = random.sample(list(self.player.skill_stats.keys()), 2)
            for skill in skills_to_train:
                improvement = random.randint(1, 2)
                self.player.skill_stats[skill] = min(100, self.player.skill_stats[skill] + improvement)
            self.player.energy -= 10
            self.player.experience += 5
            self.player.form = min(100, self.player.form + random.randint(1, 3))
            trained_skills = ", ".join(skills_to_train)
            print(f"Your skills {trained_skills} have each improved by 1-2 points.")
        else:
            print("Not enough energy for light training. Consider resting.")


    def play_match(self):
        opponent = random.choice([club for club in self.available_clubs if club != self.current_club])
        print(f"\n🏟️ Your next match is against {opponent.name}! 🏟️")
        print(f"Opponent Skill Level: {opponent.skill_level}")
        print(f"Player's Club Skill Level: {self.current_club.skill_level}")
        print(f"Your Current Skill Level: {self.player.skill_level}")
        input("Press Enter to start the match...")
        team_average_skill = (self.player.skill_stats['Shooting'] + self.player.skill_stats['Passing'] +
                            self.player.skill_stats['Dribbling'] + self.player.skill_stats['Defending']) / 4
        overall_team_skill = (team_average_skill + self.current_club.skill_level) / 2
        if overall_team_skill <= opponent.skill_level * 0.75:
            shooting_opportunities = random.randint(0, 2)
        elif overall_team_skill <= opponent.skill_level * 0.9:
            shooting_opportunities = random.randint(1, 2)
        elif overall_team_skill <= opponent.skill_level * 1.1:
            shooting_opportunities = random.randint(1, 4)
        elif overall_team_skill <= opponent.skill_level * 1.25:
            shooting_opportunities = random.randint(1, 5)
        else:
            shooting_opportunities = random.randint(2, 6)

        self.match_simulation(opponent, shooting_opportunities)

    def match_simulation(self, opponent, shooting_opportunities):
        print("\n🏟️ ---- The match is starting! ---- 🏟️")
        time.sleep(1)

        player_team_score = 0
        opponent_team_score = 0
        player_performance = 0
        goals = 0
        assists = 0
        yellow_cards = 0
        red_card = False
        injury = False
        for minute in range(1, 91):
            if minute == 45:
                print("\n⏱️  Halftime! Take a short break and review your strategy. ⏱️")
                self.halftime_team_talk()
                time.sleep(2)

            if random.random() < 0.05:
                if random.random() < 0.5 * (opponent.skill_level / (opponent.skill_level + self.current_club.skill_level + self.player.skill_level)):
                    opponent_team_score += 1
                    print(random.choice([
                        f"\n⚽ Minute {minute}: The crowd gasps as the opponent finds the back of the net!",
                        f"\n⚽ Minute {minute}: The defense falters, and the opponent capitalizes with a goal!",
                        f"\n⚽ Minute {minute}: Despite your best efforts, the opponent manages to score...",
                        f"\n⚽ Minute {minute}: The ball slips past your keeper and into the goal... What a blow!",
                        f"\n⚽ Minute {minute}: The opponent seizes the moment and scores. The tide is turning!",
                        f"\n⚽ Minute {minute}: The opposition breaks through and finds the goal. A tough moment!"
                    ]))
                elif random.random() < 0.5 * ((self.current_club.skill_level + self.player.skill_level) / (opponent.skill_level + self.current_club.skill_level + self.player.skill_level)):
                    player_team_score += 1
                    print(f"\n⏱️  Minute {minute}: 🎉 Your team scores! 🎉")

            if random.random() < 0.1 and shooting_opportunities > 0: 
                event = self.generate_match_event(opponent.skill_level, minute)
                print(f"\n⚽ Minute {minute}: {event[0]}")

                if "Decision" in event[0]:
                    outcome, performance_impact = self.handle_player_decision(event)
                    player_performance += performance_impact
                    shooting_opportunities -= 1

                    if "goal!" in outcome.lower():
                        goals += 1
                        player_team_score += 1
                    
                    if "assist!" in outcome.lower():
                        assists += 1
                        player_team_score +=1

                    if "yellow card" in outcome.lower():
                        yellow_cards += 1

            if minute % 15 == 0:
                print(f"\n⏱️  Minute {minute}: Current score is {self.current_club.name} {player_team_score} - {opponent_team_score} {opponent.name}")

            time.sleep(1) 

        print("\n🔚 The match is over! 🔚")
        print(f"Final score: {self.current_club.name} {player_team_score} - {opponent_team_score} {opponent.name}")


        self.display_match_stats(player_performance, yellow_cards, red_card, injury, goals, assists)
        self.update_player_after_match(player_team_score > opponent_team_score, player_performance, injury, goals, assists)
        self.update_league_table(player_team_score, opponent_team_score, opponent.name)

    def generate_match_event(self, opponent_strength, minute):
        events = {
            "Goalkeeper": [
                (f"Opponent is through on goal. Decision: Stay on line (1) or Rush out (2)?", 0.3),
                (f"The opponent takes a shot from distance. Decision: Dive (1) or Stay standing (2)?", 0.2),
                (f"The ball is in the box. Decision: Punch (1) or Catch (2)?", 0.2),
                (f"Your team scored a goal!", 0.1),
                (f"The opponent team scored a goal.", 0.1)
            ],
            "Defender": [
                (f"Opponent is attacking. Decision: Tackle (1) or Hold position (2)?", 0.3),
                (f"The opponent plays a long ball. Decision: Head clear (1) or Pass back to keeper (2)?", 0.2),
                (f"Your team has a corner. Decision: Go up for the corner (1) or Stay back (2)?", 0.2),
                (f"Your team scored a goal!", 0.1),
                (f"The opponent team scored a goal.", 0.1)
            ],
            "Midfielder": [
                (f"You have the ball in midfield. Decision: Pass (1) or Dribble (2)?", 0.3),
                (f"You see a teammate making a run. Decision: Through ball (1) or Hold possession (2)?", 0.2),
                (f"You have a free kick. Decision: Shoot (1) or Pass (2)?", 0.2),
                (f"Your team scored a goal!", 0.1),
                (f"The opponent team scored a goal.", 0.1)
            ],
            "Forward": [
                (f"You're one-on-one with the keeper. Decision: Shoot (1) or Dribble (2)?", 0.3),
                (f"You're on the edge of the box. Decision: Shoot (1) or Pass (2)?", 0.2),
                (f"You receive a cross. Decision: Header (1) or Volley (2)?", 0.2),
                (f"Your team scored a goal!", 0.1),
                (f"The opponent team scored a goal.", 0.1)
            ]
        }
        general_events = [
            (f"You're in a tackle situation. Decision: Go in hard (1) or Play it safe (2)?", 0.1),
            (f"The referee calls a foul. Decision: Argue (1) or Accept (2)?", 0.1),
            (f"You notice a tactical weakness. Decision: Inform coach (1) or Adjust yourself (2)?", 0.1)
        ]
        
        events[self.player.position].extend(general_events)
        if minute > 75:
            events[self.player.position].append((f"Your team needs a goal. Decision: Take a risk (1) or Play it safe (2)?", 0.2))
        return random.choices(events[self.player.position], weights=[e[1] for e in events[self.player.position]])[0]

    def handle_player_decision(self, event):
            print(f"\n{event[0]}")
            choice = self.get_input("Your choice (1 or 2): ", [1, 2])
            if "Shoot" in event[0] or "Header" in event[0] or "Volley" in event[0]:
                suspense_level = "high"
            elif "Pass" in event[0]:
                suspense_level = "medium"
            elif "Dribble" in event[0]:
                suspense_level = "low"
            elif "Tackle" in event[0]:
                suspense_level = "high"
            else:
                suspense_level = "low"
            self.generate_suspense(suspense_level)

            performance_impact = 0
            outcome = ""

            if "Shoot" in event[0] and "Pass" in event[0]:
                    if choice == 1:
                        outcome = self.determine_shoot_outcome()
                    elif choice == 2:
                        outcome = self.determine_pass_outcome()
            elif "Shoot" in event[0] and "Dribble" in event[0]:
                    if choice == 1:
                        outcome = self.determine_shoot_outcome()
                    elif choice == 2:
                        outcome = self.determine_dribble_outcome()
            elif "Header" in event[0] and "Volley" in event[0]:
                    if choice == 1:
                        outcome = self.determine_header_outcome()
                    elif choice == 2:
                        outcome = self.determine_volley_outcome()
            elif "Tackle" in event[0]:
                if choice == 1:
                    outcome = self.determine_tackle_outcome(hard=True)
                else:
                    outcome = self.determine_tackle_outcome(hard=False)
            elif "Tactical" in event[0]:
                if choice == 1:
                    outcome = self.determine_tactical_outcome(inform=True)
                elif choice == 2:
                    outcome = self.determine_tactical_outcome(inform=False)
            elif "Cross" in event[0]:
                outcome = self.determine_cross_outcome()

            print(outcome)
            performance_impact = self.calculate_performance_impact(outcome)

            return outcome, performance_impact

    def generate_suspense(self, level):
        suspense_texts = {
            "high": [
                "\nYou make your move...", "\nThe crowd holds its breath...", 
                "\nTime seems to slow down...", "\nEvery eye in the stadium is on you...",
                "\nYour heartbeat echoes in your ears...", "\nThe tension is palpable..."
            ],
            "medium": [
                "\nYou decide quickly...", "\nThe tension builds...", 
                "\nEveryone watches closely...", "\nYou make your decision...", 
                "\nThe moment of truth approaches...", "\nThe fans lean forward in anticipation..."
            ],
            "low": [
                "\nYou take the ball confidently...", 
                "\nYou weave past the defender effortlessly...",
                "\nThe play flows smoothly as you make your move..."
            ],
            "none": [
                "\nYou approach the referee furiously...", 
                "\nHeated words are exchanged...",
                "\nHe takes a step back, stopping the argument...",
            ],
        }

        suspense_art = {
            "high": ["⚽    ", "  ⚽  ", "    ⚽", "  ⚽  ", "⚽    "],
            "medium": ["⚽   ", " ⚽  ", "  ⚽ ", " ⚽  ", "⚽   "],
            "low": ["⚽  ", " ⚽ ", "⚽  "],
            "none":["🔴  ", " 🔴 ", "🔴  "]
        }

        selected_texts = random.sample(suspense_texts[level], 2 if level == "low" else 3)
        selected_art = suspense_art[level]

        for i in range(len(selected_texts)):
            print(selected_texts[i])
            for frame in selected_art:
                print(frame, end="\r")
                time.sleep(0.3 if level == "low" else 0.5 if level == "high" else 0.4)
            print("\n")

    def determine_argument_outcome(self):
        if random.random() < 0.5:
            return random.choice([
                "The referee listens to your argument but stands by the decision.",
                "Your passionate argument doesn't get you anywhere. The game goes on.",
                "The referee warns you to calm down, but the decision stands.",
                "Your argument falls on deaf ears. The game continues."
            ])
        else:
            return random.choice([
                "Your heated argument results in a yellow card. The referee is not pleased!",
                "The referee shows you a yellow card for dissent. You need to calm down!",
                "The referee is furious with your argument and shows you a yellow card!",
                "A simple argument turns into a heated exchange, and you receive a yellow card!"
            ])

    def determine_pass_outcome(self):
        if random.random() < (self.player.skill_stats['Passing'] / 100):
            return random.choice([
                "ASSIST! Your brilliant pass cuts through the defense, leading to a powerful GOAL. The crowd erupts in celebration!",
                "ASSIST! Your incisive through ball breaks the defense, allowing your teammate to calmly score the GOAL. The crowd goes wild, applauding your vision!",
                "ASSIST! Your clever backheel catches the defenders off guard, setting up a clean finish for the GOAL. The stadium roars with excitement!",
                "ASSIST! Your precise pass opens up space, leading to a brilliant GOAL. The fans explode with joy, cheering your key contribution!"
            ])
        else:
             return random.choice([
                "Missed Opportunity! Your pass is intercepted by a defender, and the attack breaks down. The fans let out a collective sigh.",
                "Your pass is on point, but the shot goes wide.Goal kick to the opponent.",
                "Your pass sails too far ahead, and your teammate can’t reach it... lost possession.",
            ])

    def determine_shoot_outcome(self):
        if random.random() < (self.player.skill_stats['Shooting'] / 100):
            return random.choice([
                "GOAL! Your shot rockets into the top corner! The crowd erupts in cheers!",
                "GOAL! You strike the ball cleanly, and it nestles into the bottom corner!",
                "GOAL! The goalkeeper dives, but your shot is unstoppable!",
                "GOAL! Your shot is perfectly placed, leaving the keeper no chance!"
            ])
        else:
            return random.choice([
                "Your powerful shot is brilliantly saved by the goalkeeper. Corner kick!",
                "Oh no! Your shot blazes over the crossbar. Goal kick to the opponent.",
                "The shot is blocked by a defender at the last second!"
            ])


    def determine_pass_outcome(self):
        return random.choice([
            "Brilliant vision! Your pass splits the defense, setting up an easy tap-in. GOAL!",
            "The defender reads your intention and intercepts the pass. The opponent counter-attacks!",
            "Safe pass. Your team maintains possession, but the chance goes begging.",
            "Your pass is inch-perfect, but your teammate is offside!",
            "The pass is a little too heavy, and it rolls out for a goal kick."
        ])

    def determine_tackle_outcome(self, hard):
        if hard:
            return random.choice([
                "You make a strong tackle and win the ball cleanly. Well done!",
                "Oh no! Your hard tackle was mistimed. The referee shows you a yellow card!",
                "Disaster! Your hard tackle results in a red card and you're sent off!",
                "You win the ball with a perfectly timed tackle, the crowd cheers your name!"
            ])
        else:
            return random.choice([
                "You play it safe and hold your position. The opponent passes the ball away.",
                "Your safe approach lets the opponent get past you. The opponent is on the attack!",
                "You gently dispossess the opponent, regaining control for your team."
            ])
    def determine_dribble_outcome(self):
        return random.choice([
            "Your dribbling skills leave the defender in the dust. You're through on goal! GOAL!",
            "The defender reads your dribble and makes a crucial interception.",
            "You weave past two defenders with a silky dribble. The crowd applauds your skill.",
            "Your dribble is too fancy, and you lose possession. The opponent counters quickly."
        ])
    
    def determine_tactical_outcome(self, inform):
        if inform:
            return random.choice([
                "You inform the coach of a tactical weakness you've noticed. The team adjusts and looks more solid.",
                "Your tactical insight helps the team regain control of the match.",
                "The coach appreciates your input and makes a crucial change. The team benefits from your observation."
            ])
        else:
            return random.choice([
                "You adjust your positioning based on your tactical awareness. The opponent struggles to break through.",
                "Your tactical adjustment pays off as the team gains momentum.",
                "Your adaptability on the field makes a difference in the team's performance."
            ])
        
    def determine_header_outcome(self):
        return random.choice([
            "Your powerful header finds the back of the net! GOAL!",
            "The goalkeeper makes a stunning save to deny your header. What a stop!",
            "Your header hits the crossbar and bounces out. So close to a goal!",
            "The defender outjumps you and clears your header. A missed opportunity."
        ])
    
    def determine_volley_outcome(self):
        return random.choice([
            "Your volley is struck sweetly and flies into the top corner! GOAL!",
            "The volley is mishit and goes wide of the goal. A disappointing effort.",
            "You connect well with the volley, but the keeper makes a fantastic save!",
            "The volley is blocked by a defender, but the ball falls kindly for a teammate to score, what an ASSIST!"
        ])
    
    def determine_cross_outcome(self):
        return random.choice([
            "Your cross is perfectly weighted, and your teammate heads it into the net! GOAL!",
            "The cross is overhit, and it sails harmlessly out of play.",
            "The defender clears your cross at the last second, preventing a goal.",
            "Your cross is blocked by a defender, but it deflects for a corner kick."
        ])


    def halftime_team_talk(self):
        print("\n----- Halftime Team Talk -----")
        print("The coach gathers the team for a halftime discussion.")
        print("What aspect of the game do you want to focus on?")
        print("1. Attacking strategy")
        print("2. Defensive organization")
        print("3. Midfield control")
        print("4. Individual motivation")
        
        choice = self.get_input("Your choice (1-4): ", range(1, 5))
        
        if choice == 1:
            print("You suggest focusing on more aggressive attacking plays.")
            self.player.skill_stats['Shooting'] += 5
            self.player.skill_stats['Dribbling'] += 3
        elif choice == 2:
            print("You emphasize the importance of maintaining a solid defensive line.")
            self.player.skill_stats['Defending'] += 5
            self.player.skill_stats['Positioning'] += 3
        elif choice == 3:
            print("You stress the need for better ball circulation in midfield.")
            self.player.skill_stats['Passing'] += 5
            self.player.skill_stats['Vision'] += 3
        else:
            print("You give a rousing speech to motivate your teammates.")
            self.player.morale += 10
            self.player.form += 5
        
        print("The team seems energized for the second half!")

    def display_match_stats(self, player_performance, yellow_cards, red_card, injury, goals, assists):
        print("\n----- Match Statistics -----")
        print(f"Player performance score: {player_performance}")
        print(f"Player goals: {goals}")
        print(f"Player assists: {assists}")
        print(f"Yellow cards: {yellow_cards}")
        print(f"Red card: {'Yes' if red_card else 'No'}")
        print(f"Injury: {'Yes' if injury else 'No'}")

    def update_player_after_match(self, won, performance_score, injury, goals, assists):
        print(f"\nMatch performance: {performance_score}")
        if won:
            print("Congratulations! You won the match!")
            self.player.morale += 15
            self.player.form += 10
        else:
            print("Unfortunately, you lost the match.")
            self.player.morale -= 10
            self.player.form -= 5
        
        if performance_score > 0:
            print("Your performance made you gain some experience.")
            self.player.experience += performance_score
        else:
            print("Your performance was subpar. You'll need to work harder in training.")

        self.player.form = max(0, min(100, self.player.form + random.randint(-10, 20)))
        self.player.morale = max(0, min(100, self.player.morale + random.randint(-10, 15)))

        if injury:
            self.player.injuries.append("Match Injury")
            self.player.energy -= 30
            print("You've sustained an injury during the match. You'll need time to recover.")

        if self.player.form <= 0:
            print("Your form has dropped significantly. Time to focus on training and rest.")
        if self.player.experience >= self.player.level * 100:
            self.player.level_up()
            
        self.player.assists += assists
        self.player.goals += goals



    def update_league_table(self, player_team_score, opponent_team_score, opponent_name):
        if player_team_score > opponent_team_score:
            self.league_table[self.current_club.name]['Points'] += 3
        elif player_team_score == opponent_team_score:
            self.league_table[self.current_club.name]['Points'] += 1
            self.league_table[opponent_name]['Points'] += 1

        self.league_table[self.current_club.name]['GF'] += player_team_score
        self.league_table[self.current_club.name]['GA'] += opponent_team_score
        self.league_table[opponent_name]['GF'] += opponent_team_score
        self.league_table[opponent_name]['GA'] += player_team_score

    def level_up(self):
        self.level += 1
        print(f"\n🎉 Congratulations! You've leveled up to level {self.level}! 🎉")
        self.experience -= (self.level - 1) * 100
        for skill in self.skill_stats:
            self.skill_stats[skill] = min(100, self.skill_stats[skill] + random.randint(1, 3))
        
        print("Your skills have improved!")
        self.view_stats()

    def view_stats(self):
        print("Viewing detailed stats.")
        print(f"Name: {self.player.name}, Position: {self.player.position}")
        print(f"Goals: {self.player.goals}, Assists: {self.player.assists}")
        print(f"Level: {self.player.level}, Experience: {self.player.experience}/{self.player.level * 100}")
        print(f"Energy: {self.player.energy}, Morale: {self.player.morale}, Form: {self.player.form}")
        print(f"Money: ${self.player.money}, Fame: {self.player.fame}")
        for skill, value in self.player.skill_stats.items():
            print(f"{skill}: {value}")

    def media_interaction(self):
        print("\n📰 Media Interview 📰")
        topics = ["personal life", "team strategy", "upcoming matches", "transfer rumors"]
        choice = self.get_input("Choose a topic to discuss: 1. Personal life, 2. Team strategy, 3. Upcoming matches, 4. Transfer rumors: ", range(1, 5))
        topic = topics[choice - 1]

        responses = {
            "personal life": ["You shared insights about your personal life. Fans feel closer to you.", 5],
            "team strategy": ["Your strategic insights showcase your deep understanding of the game.", 10],
            "upcoming matches": ["Discussing upcoming matches excites the fans and media.", 7],
            "transfer rumors": ["Your comments on transfer rumors have sparked widespread speculation.", 15]
        }

        print(responses[topic][0])
        self.player.fame += responses[topic][1]
        self.player.morale += random.randint(-5, 10)

    def view_achievements(self):
        print("Viewing achievements.")
        if self.achievements:
            for achievement in self.achievements:
                print(f"🏆 {achievement}")
        else:
            print("No achievements yet. Keep playing to earn achievements!")

    def view_league_table(self):
        print("\n----- League Table -----")
        sorted_table = sorted(self.league_table.items(), key=lambda x: (x[1]['Points'], x[1]['GF'] - x[1]['GA']), reverse=True)
        print("Pos | Team | Points | GF | GA | GD")
        for i, (team, stats) in enumerate(sorted_table, 1):
            gd = stats['GF'] - stats['GA']
            print(f"{i:2d}  | {team[:15]:15} | {stats['Points']:6d} | {stats['GF']:2d} | {stats['GA']:2d} | {gd:3d}")

    def exit_game(self):
        print("Thanks for playing Soccer Superstar! Your legacy will be remembered.")
        self.running = False

    def get_input(self, prompt, valid_options):
        while True:
            user_input = input(prompt).strip()
            try:
                selected_option = int(user_input)
                if selected_option in valid_options:
                    return selected_option
                else:
                    raise ValueError
            except ValueError:
                print("Invalid option. Please try again.")

    def advance_week(self):
        self.current_date += datetime.timedelta(days=7)
        print(f"Next week: {self.current_date}")
        self.check_season_end()

    def check_season_end(self):
        if self.current_date.month == 5 and self.current_date.day >= 15:
            self.end_season()

    def end_season(self):
        print(f"\n🏆 End of Season {self.season} 🏆")
        self.view_league_table()
        self.season += 1
        self.player.level += 1
        print(f"\nCongratulations! You've leveled up to level {self.player.level}!")
        self.reset_league_table()
        self.current_date = self.current_date.replace(month=8, day=1)
        print(f"\nWelcome to Season {self.season}! The new season begins on {self.current_date}")

    def reset_league_table(self):
        for team in league_table:
            self.league_table[team] = {'Points': 0, 'GF': 0, 'GA': 0}

    @staticmethod
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    game = SoccerCareer()
    game.start_game()
