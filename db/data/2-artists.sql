-- --------------------------------------------------------
-- Host:                         C:\Users\Hybrys\Documents\GitHub\NCSpring2022Portfolio\database.db
-- Server version:               3.38.2
-- Server OS:                    
-- HeidiSQL Version:             11.3.0.6462
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES  */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

\connect database

-- Dumping structure for table database.artists
CREATE TABLE IF NOT EXISTS artists (artist_id SERIAL PRIMARY KEY, name TEXT, isparsed BOOLEAN, UNIQUE(name));

-- Dumping data for table database.artists: -1 rows
/*!40000 ALTER TABLE "artists" DISABLE KEYS */;
INSERT INTO "artists" ("artist_id", "name", "isparsed") VALUES
	(1, 'Bright Eyes', True),
	(2, 'A Change of Pace', True),
	(3, 'A Day to Remember', True),
	(4, 'Acceptance', True),
	(5, 'Acroma', True),
	(6, 'All Time Low', True),
	(7, 'Amber Pacific', True),
	(8, 'Anberlin', True),
	(9, 'Armor For Sleep', True),
	(10, 'Army of Me', True),
	(11, 'Ashes Divide', True),
	(12, 'Atreyu', True),
	(13, 'Automatic Loveletter', True),
	(14, 'Band of Horses', True),
	(15, 'Blameshift', True),
	(16, 'Bleed the Dream', True),
	(17, 'Bloc Party', True),
	(18, 'Boys Like Girls', True),
	(19, 'Brand New', True),
	(20, 'Cartel', True),
	(21, 'Coheed and Cambria', True),
	(22, 'Coldplay', True),
	(23, 'Copeland', True),
	(24, 'Crash Test Dummies', True),
	(25, 'Cute Is What We Aim For', True),
	(26, 'Daft Punk', True),
	(27, 'Dashboard Confessional', True),
	(28, 'Death Cab for Cutie', True),
	(29, 'Electric Light Orchestra', True),
	(30, 'Fall Out Boy', True),
	(31, 'Finch', True),
	(32, 'Fleetwood Mac', True),
	(33, 'Flyleaf', True),
	(34, 'Foo Fighters', True),
	(35, 'Foster the People', True),
	(36, 'Four Year Strong', True),
	(37, 'Further Seems Forever', True),
	(38, 'Great Big Sea', True),
	(39, 'Halifax', True),
	(40, 'Hidden in Plain View', True),
	(41, 'Hit The Lights', True),
	(42, 'Interpol', True),
	(43, 'Jack''s Mannequin', True),
	(44, 'Jimmy Eat World', True),
	(45, 'Linkin Park', True),
	(46, 'LoveHateHero', True),
	(47, 'Madeon', True),
	(48, 'Mayday Parade', True),
	(49, 'Meg & Dia', True),
	(50, 'Metric', True),
	(51, 'MGMT', True),
	(52, 'Motion City Soundtrack', True),
	(53, 'Mumford & Sons', True),
	(54, 'Mute Math', True),
	(55, 'My American Heart', True),
	(56, 'New Found Glory', True),
	(57, 'Nightwish', True),
	(58, 'Nine Inch Nails', True),
	(59, 'Number One Gun', True),
	(60, 'Oasis', True),
	(61, 'OK Go', True),
	(62, 'Owl City', True),
	(63, 'Paramore', True),
	(64, 'Park', True),
	(65, 'Paul Hartnoll', True),
	(66, 'Paul Simon', True),
	(67, 'Pink Floyd', True),
	(68, 'Punchline', True),
	(69, 'Quietdrive', True),
	(70, 'Red Hot Chili Peppers', True),
	(71, 'Relient K', True),
	(72, 'Rise Against', True),
	(73, 'Run Kid Run', True),
	(74, 'Rush', True),
	(75, 'Saosin', True),
	(76, 'Say Anything', True),
	(77, 'Scissor Sisters', True),
	(78, 'Search the City', True),
	(79, 'Senses Fail', True),
	(80, 'Silverstein', True),
	(81, 'Snow Patrol', True),
	(82, 'Something Corporate', True),
	(83, 'Spin Doctors', True),
	(84, 'Spitalfield', True),
	(85, 'Story of the Year', True),
	(86, 'Sugarcult', True),
	(87, 'Switchfoot', True),
	(88, 'Taking Back Sunday', True),
	(89, 'Taylor Swift', True),
	(90, 'Ten Second Epic', True),
	(91, 'Tenacious D', True),
	(92, 'The Academy Is...', True),
	(93, 'The Arcade Fire', True),
	(94, 'The Black Keys', True),
	(95, 'The Black Mages', True),
	(96, 'The Cat Empire', True),
	(97, 'The Classic Crime', True),
	(98, 'The Early November', True),
	(99, 'The Get Up Kids', True),
	(100, 'The Juliana Theory', True),
	(101, 'The Killers', True),
	(102, 'The Maine', True),
	(103, 'The Postal Service', True),
	(104, 'The Rocket Summer', True),
	(105, 'The Starting Line', True),
	(106, 'The Summer Obsession', True),
	(107, 'The Working Title', True),
	(108, 'Thrice', True),
	(109, 'Thursday', True),
	(110, 'Tonight Alive', True),
	(111, 'Trust Company', True),
	(112, 'We The Kings', True),
	(113, 'Weezer', True),
	(114, 'Yellowcard', True),
	(115, 'The Beatles', True),
	(116, 'The Rolling Stones', True),
	(117, 'Bob Dylan', True),
	(118, 'David Bowie', True),
	(119, 'Led Zeppelin', True),
	(120, 'Bruce Springsteen', True),
	(121, 'Prince', True),
	(122, 'The Who', True),
	(123, 'Elvis Presley', True),
	(124, 'Jimi Hendrix', True),
	(125, 'The Beach Boys', True),
	(126, 'R.E.M.', True),
	(127, 'The Velvet Underground', True),
	(128, 'Marvin Gaye', True),
	(129, 'U2', True),
	(130, 'The Clash', True),
	(131, 'Nirvana', True),
	(132, 'Radiohead', True),
	(133, 'Neil Young', True),
	(134, 'Stevie Wonder', True),
	(135, 'Elvis Costello', True),
	(136, 'Bob Marley and The Wailers', True),
	(137, 'Van Morrison', True),
	(138, 'Aretha Franklin', True),
	(139, 'Talking Heads', True),
	(140, 'The Smiths', True),
	(141, 'The Byrds', True),
	(142, 'Public Enemy', True),
	(143, 'The Doors', True),
	(144, 'Miles Davis', True),
	(145, 'James Brown', True),
	(146, 'The Kinks', True),
	(147, 'Beastie Boys', True),
	(148, 'Creedence Clearwater Revival', True),
	(149, 'Otis Redding', True),
	(150, 'Michael Jackson', True),
	(151, 'Beck', True),
	(152, 'Sex Pistols', True),
	(153, 'Sly and the Family Stone', True),
	(154, 'Roxy Music', True),
	(155, 'Johnny Cash', True),
	(156, 'John Lennon', True),
	(157, 'Pixies', True),
	(158, 'Joni Mitchell', True),
	(159, 'Blur', True),
	(160, 'Ramones', True),
	(161, 'Madonna', True),
	(162, 'Lou Reed', True),
	(163, 'Sonic Youth', True),
	(164, 'Simon and Garfunkel', True),
	(165, 'Joy Division', True),
	(166, 'OutKast', True),
	(167, 'The Band', True),
	(168, 'New Order', True),
	(169, 'Ray Charles', True),
	(170, 'The Police', True),
	(171, 'Kraftwerk', True),
	(172, 'Al Green', True),
	(173, 'Steely Dan', True),
	(174, 'John Coltrane', True),
	(175, 'P J Harvey', True),
	(176, 'Björk', True),
	(177, 'Massive Attack', True),
	(178, 'The Jam', True),
	(179, 'Chuck Berry', True),
	(180, 'The Stooges', True),
	(181, 'Tom Waits', True),
	(182, 'The White Stripes', True),
	(183, 'Eminem', True),
	(184, 'Frank Sinatra', True),
	(185, 'The Cure', True),
	(186, 'Metallica', True),
	(187, 'Brian Eno', True),
	(188, 'Buddy Holly & The Crickets', True),
	(189, 'Captain Beefheart and His Magic Band', True),
	(190, 'Black Sabbath', True),
	(191, 'Guns ''n'' Roses', True),
	(192, 'Nick Cave', True),
	(193, 'Primal Scream', True),
	(194, 'Pavement', True),
	(195, 'Missy Misdemeanor Elliott', True),
	(196, 'Patti Smith', True),
	(197, 'Little Richard', True),
	(198, 'Pulp', True),
	(199, 'The Eagles', True),
	(200, 'Elton John', True),
	(201, 'Run-D.M.C.', True),
	(202, 'Blondie', True),
	(203, 'Leonard Cohen', True),
	(204, 'Grateful Dead', True),
	(205, 'Nick Drake', True),
	(206, 'The Temptations', True),
	(207, 'Pet Shop Boys', True),
	(208, 'Franz Ferdinand', True),
	(209, 'T. Rex', True),
	(210, 'Hüsker Dü', True),
	(211, 'Thelonious Monk', True),
	(212, 'Wilco', True),
	(213, 'The Smashing Pumpkins', True),
	(214, 'Charles Mingus', True),
	(215, 'Rod Stewart', True),
	(216, 'Pearl Jam', True),
	(217, 'Sam Cooke', True),
	(218, 'Aerosmith', True),
	(219, 'Duke Ellington', True),
	(220, 'Queen', True),
	(221, 'The Everly Brothers', True),
	(222, 'Randy Newman', True),
	(223, 'Muddy Waters', True),
	(224, 'Cream', True),
	(225, 'The Jesus and Mary Chain', True),
	(226, 'The Strokes', True),
	(227, 'The Chemical Brothers', True),
	(228, 'The Specials', True),
	(229, 'The Stone Roses', True),
	(230, 'Smokey Robinson and The Miracles', True),
	(231, 'Kate Bush', True),
	(232, 'Kanye West', True),
	(233, 'Pretenders', True),
	(234, 'My Bloody Valentine', True),
	(235, 'Jefferson Airplane', True),
	(236, 'Crosby, Stills, Nash (& Young)', False),
	(237, 'Big Star', True),
	(238, 'Grandmaster Flash', True),
	(239, 'Roy Orbison', True),
	(240, 'Television', True),
	(241, 'Deep Purple', True),
	(242, 'Jay-Z', True),
	(243, 'The Replacements', True),
	(244, 'The Flaming Lips', True),
	(245, 'Peter Gabriel', True),
	(246, 'Sonny Rollins', True),
	(247, 'De La Soul', True),
	(248, 'Ornette Coleman', True),
	(249, 'The Streets', True),
	(250, 'The Verve', True),
	(251, 'Curtis Mayfield', True),
	(252, 'Santana', True),
	(253, 'Morrissey', True),
	(254, 'Derek and The Dominos', True),
	(255, 'The Supremes', True),
	(256, 'Dr. Dre', True),
	(257, 'Manic Street Preachers', True),
	(258, 'Yo La Tengo', True),
	(259, 'XTC', True),
	(260, 'Lynyrd Skynyrd', True),
	(261, 'Jackson Browne', True),
	(262, 'Depeche Mode', True),
	(263, 'Carole King', True),
	(264, 'Hank Williams', True),
	(265, 'Ella Fitzgerald', True),
	(266, 'Love', True),
	(267, 'Chic', True),
	(268, 'Jerry Lee Lewis', True),
	(269, 'Portishead', True),
	(270, 'Can', True),
	(271, 'A Tribe Called Quest', True),
	(272, 'King Crimson', True),
	(273, 'The Prodigy', True),
	(274, 'Herbie Hancock', True),
	(275, 'Queens of the Stone Age', True),
	(276, 'Van Halen', True),
	(277, 'Suede', True),
	(278, 'The Four Tops', True),
	(279, 'LL Cool J', True),
	(280, 'Eric B. & Rakim', True),
	(281, 'Dusty Springfield', True),
	(282, 'Echo and the Bunnymen', True),
	(283, 'Underworld', True),
	(284, 'The Bee Gees', True),
	(285, 'The Allman Brothers Band', True),
	(286, 'Public Image Ltd.', True),
	(287, 'Wire', True),
	(288, 'Tom Petty', True),
	(289, 'Happy Mondays', True),
	(290, 'Iggy Pop', True),
	(291, 'N.W.A.', True),
	(292, 'Elliott Smith', True),
	(293, 'Motörhead', True),
	(294, 'The Isley Brothers', True),
	(295, 'Bo Diddley', True),
	(296, 'Gram Parsons', True),
	(297, 'Soundgarden', True),
	(298, 'Notorious B.I.G.', True),
	(299, 'Belle and Sebastian', True),
	(300, 'Jimmy Cliff', True),
	(301, 'Howlin'' Wolf', True),
	(302, 'Basement Jaxx', True),
	(303, 'Jane''s Addiction', True),
	(304, 'ABBA', True),
	(305, 'Tricky', True),
	(306, 'Dexy''s Midnight Runners', True),
	(307, 'The Human League', True),
	(308, 'Buffalo Springfield', True),
	(309, 'Dire Straits', True),
	(310, 'Sinéad O''Connor', True),
	(311, 'TLC', True),
	(312, 'Green Day', True),
	(313, 'Nico', True),
	(314, 'Aphex Twin', True),
	(315, 'Fugazi', True),
	(316, 'Stan Getz', True),
	(317, 'Gorillaz', True),
	(318, 'Tim Buckley', True),
	(319, 'Lucinda Williams', True),
	(320, 'Scott Walker', True),
	(321, 'New York Dolls', True),
	(322, 'Donna Summer', True),
	(323, 'Sufjan Stevens', True),
	(324, 'Fairport Convention', True),
	(325, 'Bill Evans', True),
	(326, 'MC5', True),
	(327, 'The Buzzcocks', True),
	(328, 'Talk Talk', True),
	(329, 'Count Basie', True),
	(330, 'The Libertines', True),
	(331, 'Richard and Linda Thompson', True),
	(332, 'The Drifters', True),
	(333, 'LCD Soundsystem', True),
	(334, 'Rage Against the Machine', True),
	(335, 'Gang of Four', True),
	(336, 'The Pogues', True),
	(337, 'Ike and Tina Turner', True),
	(338, 'Fats Domino', True),
	(339, 'Dizzee Rascal', True),
	(340, 'The Ronettes', True),
	(341, 'Todd Rundgren', True),
	(342, 'Modest Mouse', True),
	(343, 'Traffic', True),
	(344, 'Lauryn Hill', True),
	(345, 'Fatboy Slim', True),
	(346, 'Alice Cooper', True),
	(347, 'Sleater-Kinney', True),
	(348, 'Willie Nelson', True),
	(349, 'Thin Lizzy', True),
	(350, 'John Cale', True),
	(351, 'Eric Clapton', True),
	(352, 'Isaac Hayes', True),
	(353, 'DJ Shadow', True),
	(354, 'Little Feat', True),
	(355, 'X', True),
	(356, 'B.B. King', True),
	(357, 'Genesis', True),
	(358, 'Jeff Buckley', True),
	(359, 'Mott the Hoople', True),
	(360, 'Yes', True),
	(361, 'Cheap Trick', True),
	(362, 'The B-52''s', True),
	(363, 'Dinosaur Jr.', True),
	(364, 'The O''Jays', True),
	(365, 'Paul McCartney and Wings', True),
	(366, 'TV on the Radio', True),
	(367, 'Billie Holiday', True),
	(368, 'Fugees', True),
	(369, 'Sigur Ros', True),
	(370, 'M.I.A.', True),
	(371, 'The Jackson 5', True),
	(372, 'Martha and The Vandellas', True),
	(373, 'James Taylor', True),
	(374, 'Wu-Tang Clan', True),
	(375, 'Air', True),
	(376, 'Billy Bragg', True),
	(377, 'Patsy Cline', True),
	(378, 'Devo', True),
	(379, 'Dion', True),
	(380, 'Robert Wyatt', True),
	(381, 'The Crystals', True),
	(382, 'The Animals', True),
	(383, 'The Righteous Brothers', True),
	(384, 'Art Blakey', True),
	(385, 'Dizzy Gillespie', True),
	(386, 'Pere Ubu', True),
	(387, 'Spiritualized', True),
	(388, 'The Kingsmen', True),
	(389, 'Kiss', True),
	(390, 'Ian Dury and The Blockheads', True),
	(391, 'Eric Dolphy', True),
	(392, 'Snoop Doggy Dogg', True),
	(393, 'Louis Armstrong', True),
	(394, 'Def Leppard', True),
	(395, 'The Fall', True),
	(396, 'Violent Femmes', True),
	(397, 'Hole', True),
	(398, 'The Breeders', True),
	(399, 'Loretta Lynn', True),
	(400, 'Supergrass', True),
	(401, 'Moby', True),
	(402, 'Mercury Rev', True),
	(403, 'Prefab Sprout', True),
	(404, 'Teenage Fanclub', True),
	(405, 'Procol Harum', True),
	(406, 'ABC', True),
	(407, 'Orbital', True),
	(408, 'Boogie Down Productions', True),
	(409, 'The Flying Burrito Brothers', True),
	(410, 'Jackie Wilson', True),
	(411, 'Charlie Parker', True),
	(412, 'Ben E. King', True),
	(413, 'The Roots', True),
	(414, 'Antony and The Johnsons', True),
	(415, 'Yeah Yeah Yeahs', True),
	(416, 'Built to Spill', True),
	(417, 'Jethro Tull', True),
	(418, 'Augustus Pablo', True),
	(419, 'Cypress Hill', True),
	(420, 'Spoon', True),
	(421, 'Suicide', True),
	(422, 'Soul II Soul', True),
	(423, 'Cyndi Lauper', True),
	(424, 'Crowded House', True),
	(425, 'Graham Parker', True),
	(426, 'Ry Cooder', True),
	(427, 'The Undertones', True),
	(428, 'George Harrison', True),
	(429, 'The Orb', True),
	(430, 'Frankie Goes to Hollywood', True),
	(431, 'Serge Gainsbourg', True),
	(432, 'Them', True),
	(433, 'The Go-Betweens', True),
	(434, 'Janet Jackson', True),
	(435, 'Tracy Chapman', True),
	(436, 'George Michael', True),
	(437, 'Bill Haley and His Comets', True),
	(438, 'Ice Cube', True),
	(439, 'Alanis Morissette', True),
	(440, 'D''Angelo', True),
	(441, 'Eurythmics', True),
	(442, 'The Mamas and the Papas', True),
	(443, 'Joe Cocker', True),
	(444, 'Stereolab', True),
	(445, 'The Small Faces', True),
	(446, 'Super Furry Animals', True),
	(447, 'Liz Phair', True),
	(448, 'The Impressions', True),
	(449, 'Faith No More', True),
	(450, 'Wayne Shorter', True),
	(451, 'Del Shannon', True),
	(452, 'Billy Joel', True),
	(453, 'Boston', True),
	(454, 'The Dead Kennedys', True),
	(455, 'Blue Oyster Cult', True),
	(456, 'The New Pornographers', True),
	(457, 'Glen Campbell', True),
	(458, 'Dave Brubeck', True),
	(459, 'The LA''s', False),
	(460, 'Booker T. & The MG''s', True),
	(461, 'The Lovin'' Spoonful', True),
	(462, 'Arctic Monkeys', True),
	(463, 'Soft Cell', True),
	(464, 'Bob Seger', True),
	(465, 'Ryan Adams', True),
	(466, 'Slayer', True),
	(467, 'The Zombies', True),
	(468, 'Woody Guthrie', True),
	(469, 'Robert Johnson', True),
	(470, 'Eddie Cochran', True),
	(471, 'Chick Corea', True),
	(472, 'The Shangri-La''s', True),
	(473, 'Cecil Taylor', True),
	(474, 'Dolly Parton', True),
	(475, 'Sun Ra', True),
	(476, 'Tori Amos', True),
	(477, 'Big Joe Turner', True),
	(478, 'The Rapture', True),
	(479, 'Wilson Pickett', True),
	(480, 'The Shins', True),
	(481, '2Pac', True),
	(482, 'ZZ Top', True),
	(483, 'Duran Duran', True),
	(484, 'Tortoise', True),
	(485, 'The The', True),
	(486, 'Ghostface Killah', True),
	(487, 'System of a Down', True),
	(488, 'Warren Zevon', True),
	(489, 'Sam and Dave', True),
	(490, 'Bonnie "Prince" Billy', True),
	(491, 'The KLF', True),
	(492, 'The Waterboys', True),
	(493, 'The Cars', True),
	(494, 'The Shirelles', True),
	(495, 'Ritchie Valens', True),
	(496, 'Los Lobos', True),
	(497, 'The Coasters', True),
	(498, 'Arrested Development', True),
	(499, 'Bon Jovi', True),
	(500, 'Harry Nilsson', True),
	(501, 'Iron Maiden', True),
	(502, 'Magazine', True),
	(503, 'Brian Wilson', True),
	(504, 'John Lee Hooker', True),
	(505, 'Cornershop', True),
	(506, 'Benny Goodman', True),
	(507, 'Afrika Bambaataa & The Soul Sonic Force', True),
	(508, 'Harold Melvin and The Bluenotes', True),
	(509, 'Bobby Bland', True),
	(510, 'Joe Jackson', True),
	(511, 'The Soft Machine', True),
	(512, 'George Jones', True),
	(513, 'Etta James', True),
	(514, 'Lee Morgan', True),
	(515, 'Emmylou Harris', True),
	(516, 'Tina Turner', True),
	(517, 'Garbage', True),
	(518, 'Sarah Vaughan', True),
	(519, 'Dionne Warwick', True),
	(520, 'Squeeze', True),
	(521, 'Bud Powell', True),
	(522, 'Cat Power', True),
	(523, 'Madness', True),
	(524, 'Keith Jarrett', True),
	(525, 'The Hives', True),
	(526, '50 Cent', True),
	(527, 'Laura Nyro', True),
	(528, 'Horace Silver', True),
	(529, 'Leftfield', True),
	(530, 'The Avalanches', True),
	(531, 'Britney Spears', True),
	(532, 'John Cougar Mellencamp', True),
	(533, 'The Monkees', True),
	(534, 'Percy Sledge', True),
	(535, 'The Platters', True),
	(536, 'Goldie', True),
	(537, 'Midnight Oil', True),
	(538, 'Mary J. Blige', True),
	(539, 'Black Flag', True),
	(540, 'Jeff Beck', True),
	(541, 'Nas', True),
	(542, 'Gene Vincent', True),
	(543, 'Magnetic Fields', True),
	(544, 'Culture Club', True),
	(545, 'Minutemen', True),
	(546, 'Richard Hell & The Voidoids', True),
	(547, 'Simple Minds', True),
	(548, 'Bad Brains', True),
	(549, 'Carl Perkins', True),
	(550, 'Laurie Anderson', True),
	(551, 'Blood, Sweat & Tears', True),
	(552, 'The Go-Go''s', True),
	(553, 'Free', True),
	(554, 'The Cult', True),
	(555, 'Toots and The Maytals', True),
	(556, 'Burning Spear', True),
	(557, 'Steve Miller Band', True),
	(558, 'My Morning Jacket', True),
	(559, 'Mike Oldfield', True),
	(560, 'Clifford Brown', True),
	(561, 'John Mayall', True),
	(562, 'Big Black', True),
	(563, 'Broken Social Scene', True),
	(564, 'Cocteau Twins', True),
	(565, 'The Feelies', True),
	(566, 'Lloyd Price', True),
	(567, 'Albert Ayler', True),
	(568, 'Neu!', True),
	(569, 'The Mahavishnu Orchestra', True),
	(570, 'Max Roach', True),
	(571, 'Beyonce', True),
	(572, 'Cat Stevens', True),
	(573, 'Deee-Lite', True),
	(574, 'Moby Grape', True),
	(575, 'Mission of Burma', True),
	(576, 'The Dandy Warhols', True),
	(577, 'Wes Montgomery', True),
	(578, 'Elastica', True),
	(579, 'k.d. Lang', True),
	(580, 'X-Ray Spex', True),
	(581, 'The Rascals', True),
	(582, 'Donald Fagen', True),
	(583, 'Grace Jones', True),
	(584, 'Mogwai', True),
	(585, 'Meat Puppets', True),
	(586, 'Kelis', True),
	(587, '13th Floor Elevators', True),
	(588, 'Linda Ronstadt', True),
	(589, 'The Flamin'' Groovies', True),
	(590, 'Guided by Voices', True),
	(591, 'Siouxsie and The Banshees', True),
	(592, 'The Beat', True),
	(593, 'Steve Earle', True),
	(594, 'Meat Loaf', True),
	(595, 'The Gun Club', True),
	(596, 'Bing Crosby', True),
	(597, 'The Spinners', True),
	(598, 'Slint', True),
	(599, 'Johnny Burnette', True),
	(600, 'Devendra Banhart', True),
	(601, 'Frankie Lymon and The Teenagers', True),
	(602, 'Travis', True),
	(603, 'The Damned', True),
	(604, 'Manu Chao', True),
	(605, 'Boards of Canada', True),
	(606, 'Modern Jazz Quartet', True),
	(607, 'Common', True),
	(608, 'Rickie Lee Jones', True),
	(609, 'Animal Collective', True),
	(610, 'Tindersticks', True),
	(611, 'Rufus Wainwright', True),
	(612, 'Desmond Dekker', True),
	(613, 'Cannonball Adderley', True),
	(614, 'Kylie Minogue', True),
	(615, 'George Russell', True),
	(616, 'Godspeed You Black Emperor!', True),
	(617, 'Aaliyah', True),
	(618, 'Solomon Burke', True),
	(619, 'The Blue Nile', True),
	(620, 'Minor Threat', True),
	(621, 'Eels', True),
	(622, 'The Yardbirds', True),
	(623, 'Garth Brooks', True),
	(624, 'The Darkness', True),
	(625, 'Judy Garland', True),
	(626, 'John Martyn', True),
	(627, 'The Sparks', True),
	(628, 'Buena Vista Social Club', True),
	(629, 'Living Colour', True),
	(630, 'Fela Kuti', True),
	(631, 'King Sunny Adé', True),
	(632, 'The Carpenters', True),
	(633, 'Neneh Cherry', True),
	(634, 'The Sugarcubes', True),
	(635, 'Lambchop', True),
	(636, 'Lloyd Cole and The Commotions', False),
	(637, 'Bonnie Raitt', True),
	(638, 'The Jungle Brothers', True),
	(639, 'Weather Report', True),
	(640, 'War', True),
	(641, 'Tammy Wynette', True),
	(642, 'Albert King', True),
	(643, 'Erykah Badu', True),
	(644, 'Ministry', True),
	(645, 'Don Henley', True),
	(646, 'Nat King Cole', True),
	(647, 'Spacemen 3', True),
	(648, '10 CC', True),
	(649, 'The Decemberists', True),
	(650, 'Oliver Nelson', True),
	(651, 'The Carter Family', True),
	(652, 'The Pop Group', True),
	(653, 'Gladys Knight and The Pips', True),
	(654, 'Blumfeld', True),
	(655, 'The Mars Volta', True),
	(656, 'Dr. John', True),
	(657, 'Gang Starr', True),
	(658, 'The Sugarhill Gang', True),
	(659, 'The Moody Blues', True),
	(660, 'Faust', True),
	(661, 'Spencer Davis Group', True),
	(662, 'Whitney Houston', True),
	(663, 'Chubby Checker', True),
	(664, 'And You Will Know Us by the Trail of Dead', False),
	(665, 'The Troggs', True),
	(666, 'Salt ''n'' Pepa', True),
	(667, 'The Birthday Party', True),
	(668, 'Phil Spector', True),
	(669, 'Nick Lowe', True),
	(670, 'Ann Peebles', True),
	(671, 'Sugar', True),
	(672, 'Joan Jett and The Blackhearts', True),
	(673, 'Kate and Anna McGarrigle', True),
	(674, 'The Chiffons', True),
	(675, 'Cameo', True),
	(676, 'The Psychedelic Furs', True),
	(677, 'Jimmy Giuffre', True),
	(678, 'The Mekons', True),
	(679, 'At the Drive-In', True),
	(680, 'Amerie', True),
	(681, 'Tool', True),
	(682, 'Question Mark and the Mysterians', True),
	(683, 'Kyuss', True),
	(684, 'Earth, Wind & Fire', True),
	(685, 'Digital Underground', True),
	(686, 'Gil Evans', True),
	(687, 'Leadbelly', True),
	(688, 'Suzanne Vega', True),
	(689, 'The Shadows', True),
	(690, 'Don McLean', True),
	(691, 'The Meters', True),
	(692, 'They Might Be Giants', True),
	(693, 'Afghan Whigs', True),
	(694, 'The Flamingos', True),
	(695, 'Paul Butterfield Blues Band', True),
	(696, 'Rick James', True),
	(697, 'Art Pepper', True),
	(698, 'John Hiatt', True),
	(699, 'Destiny''s Child', True),
	(700, 'The Five Satins', True),
	(701, 'Erroll Garner', True),
	(702, 'Fine Young Cannibals', True),
	(703, 'Tears for Fears', True),
	(704, 'Lee Perry', True),
	(705, '808 State', True),
	(706, 'Art Brut', True),
	(707, 'Culture', True),
	(708, 'The Orioles', True),
	(709, 'Nelly', True),
	(710, 'Alicia Keys', True),
	(711, 'Gnarls Barkley', True),
	(712, 'The Jayhawks', True),
	(713, 'Neutral Milk Hotel', True),
	(714, 'Boz Scaggs', True),
	(715, 'Quicksilver Messenger Service', True),
	(716, 'Kaiser Chiefs', True),
	(717, 'Rahsaan Roland Kirk', True),
	(718, 'Steppenwolf', True),
	(719, 'Doves', True),
	(720, 'The Notwist', True),
	(721, 'Sheryl Crow', True),
	(722, 'The Faces', True),
	(723, 'Henry Mancini', True),
	(724, 'Bill Withers', True),
	(725, 'The Boo Radleys', True),
	(726, 'Alice in Chains', True),
	(727, 'Scritti Politti', True),
	(728, 'Japan', True),
	(729, 'The Congos', True),
	(730, 'The Incredible String Band', True),
	(731, 'The Four Seasons', True),
	(732, 'Harry Belafonte', True),
	(733, 'Badly Drawn Boy', True),
	(734, 'Justin Timberlake', True),
	(735, 'Joe Henderson', True),
	(736, 'Ruben Bladés', True),
	(737, 'Jimmy Smith', True),
	(738, 'Lenny Kravitz', True),
	(739, 'Dexter Gordon', True),
	(740, 'The Neville Brothers', True),
	(741, 'R. Kelly', True),
	(742, 'Judas Priest', True),
	(743, 'Placebo', True),
	(744, 'Townes Van Zandt', True),
	(745, 'David Sylvian', True),
	(746, 'Archie Shepp', True),
	(747, 'The Slits', True),
	(748, 'The Lemonheads', True),
	(749, 'Linton Kwesi Johnson', True),
	(750, 'Madvillain', True),
	(751, 'Bill Monroe', True),
	(752, 'Sebadoh', True),
	(753, 'Fountains of Wayne', True),
	(754, 'Bessie Smith', True),
	(755, 'Nina Simone', True),
	(756, 'Low', True),
	(757, 'Jon Spencer Blues Explosion', True),
	(758, 'Raekwon', True),
	(759, 'Little Willie John', True),
	(760, 'The Teardrop Explodes', True),
	(761, 'Inner City', True),
	(762, 'The Saints', True),
	(763, 'N.E.R.D.', True),
	(764, 'Coolio', True),
	(766, 'The Box Tops', True),
	(767, 'The Nitty Gritty Dirt Band', True),
	(768, 'Marty Robbins', True),
	(769, 'Average White Band', True),
	(770, 'Liars', True),
	(771, 'Black Rebel Motorcycle Club', True),
	(772, 'The Beta Band', True),
	(773, 'Glenn Miller', True),
	(774, 'Maximo Park', True),
	(775, 'Lester Young', True),
	(776, 'Röyksopp', True),
	(777, 'The Associates', True),
	(778, 'Gloria Gaynor', True),
	(779, 'Screamin'' Jay Hawkins', True),
	(780, 'Destroyer', True),
	(781, 'Matthew Sweet', True),
	(782, 'Ol'' Dirty Bastard', True),
	(783, 'Sister Sledge', True),
	(784, 'A Guy Called Gerald', True),
	(785, 'Anita Baker', True),
	(786, 'Fehlfarben', True),
	(787, 'Butthole Surfers', True),
	(788, 'Mobb Deep', True),
	(789, 'John Prine', True),
	(790, 'Young Marble Giants', True),
	(791, 'Stiff Little Fingers', True),
	(792, 'Pat Metheny', True),
	(793, 'Lambert, Hendricks and Ross', True),
	(794, 'EPMD', True),
	(795, 'The Penguins', True),
	(796, 'Stereo MC''s', True),
	(797, 'Norah Jones', True),
	(798, 'Kelly Clarkson', True),
	(799, 'The Dream Syndicate', True),
	(800, 'Spirit', True),
	(801, 'Gene Autry', True),
	(802, 'David Crosby', True),
	(803, 'Jackie Brenston', True),
	(804, 'Method Man', True),
	(805, 'The Black Crowes', True),
	(806, 'The Art Ensemble of Chicago', True),
	(807, 'Supertramp', True),
	(808, 'Joao Gilberto', True),
	(809, 'Everything But the Girl', True),
	(810, 'Sting', True),
	(811, 'Bobby Darin', True),
	(812, 'Link Wray', True),
	(813, 'Rob Base & DJ E-Z Rock', True),
	(814, 'The Only Ones', True),
	(815, 'Yoko Ono', True),
	(816, 'The Staple Singers', True),
	(817, 'Edwin Starr', True),
	(818, 'Youssou N''Dour', True),
	(819, 'The Futureheads', True),
	(820, 'Jackie McLean', True),
	(821, 'McCoy Tyner', True),
	(822, 'Wilbert Harrison', True),
	(823, 'Fats Waller', True),
	(824, 'Elmore James', True),
	(825, 'Stardust', True),
	(826, 'James Carr', True),
	(827, 'Doug E. Fresh', True),
	(828, 'Uncle Tupelo', True),
	(829, 'Bad Company', True),
	(830, 'Marianne Faithfull', True),
	(831, 'Neko Case', True),
	(832, 'Shania Twain', True),
	(833, 'Sublime', True),
	(834, 'Jimmy Reed', True),
	(835, 'Aztec Camera', True),
	(836, 'PM Dawn', True),
	(837, 'Steve Reich', True),
	(838, 'Slade', True),
	(839, 'Bobbie Gentry', True),
	(840, 'The Original Soundtrack', True),
	(841, 'The Soft Boys', True),
	(842, '"Tennessee" Ernie Ford', True),
	(843, 'Little Eva', True),
	(844, 'Black Uhuru', True),
	(845, 'Electric Six', True),
	(846, 'Autechre', True),
	(847, 'The Chi-Lites', True),
	(848, 'The Cramps', True),
	(849, 'Barbra Streisand', True),
	(850, 'Diana Ross', True),
	(851, 'Cliff Richard', True),
	(852, 'The Raincoats', True),
	(853, 'Korn', True),
	(854, 'Palace Brothers', True),
	(855, 'Le Mystère des Voix Bulgares', True),
	(856, 'John Zorn', True),
	(857, 'Junior Wells'' Chicago Blues Band', False),
	(858, 'Phil Collins', True),
	(859, 'Tangerine Dream', True),
	(860, 'Freda Payne', True),
	(861, 'Pete Rock and CL Smooth', True),
	(862, 'Gwen Stefani', True),
	(863, 'L7', True),
	(864, 'Merle Haggard', True),
	(865, 'Grandaddy', True),
	(866, 'Van Dyke Parks', True),
	(867, 'Sepultura', True),
	(868, 'The Walker Brothers', True),
	(869, 'Alexander Skip Spence', False),
	(870, 'Caetano Veloso', True),
	(871, 'Sam the Sham and The Pharaos', False),
	(872, 'Gene Chandler', True),
	(873, 'The Residents', True),
	(874, 'Fiona Apple', True),
	(875, 'Junior Boys', True),
	(876, 'Naughty by Nature', True),
	(877, 'Killing Joke', True),
	(878, 'Gary Numan', True),
	(879, 'Fred Neil', True),
	(880, 'The Pharcyde', True),
	(881, 'Gene Clark', True),
	(882, 'Camper Van Beethoven', True),
	(883, 'Beth Orton', True),
	(884, 'The Sonics', True),
	(885, 'This Mortal Coil', True),
	(886, 'Cowboy Junkies', True),
	(887, 'Ricky Nelson', True),
	(888, 'The Weavers', True),
	(889, 'The Microphones', True),
	(890, 'Foreigner', True),
	(891, 'Bauhaus', True),
	(892, 'The Last Poets', True),
	(893, 'Syd Barrett', True),
	(894, 'Wolf Parade', True),
	(895, 'Terry Riley', True),
	(896, 'The Coral', True),
	(897, 'Marilyn Manson', True),
	(898, 'Ash', True),
	(899, 'Pentangle', True),
	(900, 'Freddie Hubbard', True),
	(901, 'Busta Rhymes', True),
	(902, 'Mary Wells', True),
	(903, 'Steve Harley & Cockney Rebel', True),
	(904, 'Waylon Jennings', True),
	(905, 'Carly Simon', True),
	(906, 'Nusrat Fateh Ali Khan', True),
	(907, 'Mos Def', True),
	(908, 'Journey', True),
	(909, 'Country Joe & The Fish', True),
	(910, 'The Screaming Trees', True),
	(911, 'Aimee Mann', True),
	(912, 'LaVern Baker', True),
	(913, 'Oscar Peterson', True),
	(914, 'The Sisters of Mercy', True),
	(915, 'Dinah Washington', True),
	(916, 'Drive-By Truckers', True),
	(917, 'Blackstreet', True),
	(918, 'Calexico', True),
	(919, 'Prefuse 73', True),
	(920, 'The Raspberries', True),
	(921, 'Andrew Hill', True),
	(923, 'INXS', True),
	(924, 'Peter Frampton', True),
	(925, 'Gerry Mulligan', True),
	(926, 'Emerson, Lake & Palmer', True),
	(927, 'Ride', True),
	(928, 'Heaven 17', True),
	(929, 'Fingers Inc.', True),
	(930, 'Sparklehorse', True),
	(931, 'The Marvelettes', True),
	(932, 'Funky Four Plus One', True),
	(933, 'Ray Price', True),
	(934, 'Hanson', True),
	(935, 'Geto Boys', True),
	(936, 'Salif Keita', True),
	(937, 'The Searchers', True),
	(938, 'Galaxie 500', True),
	(939, 'The Stranglers', True),
	(940, 'The Left Banke', True),
	(941, 'Buju Banton', True),
	(942, 'Jimmie Rodgers', True),
	(943, 'Daryl Hall and John Oates', True),
	(944, 'Disposable Heroes of Hiphoprisy', True),
	(945, 'Womack and Womack', True),
	(946, 'New Radicals', True),
	(947, 'Nancy Sinatra', True),
	(948, 'Willie Mae "Big Mama" Thornton', False),
	(949, 'Urge Overkill', True),
	(950, 'Milt Jackson', True),
	(951, 'Bunny Wailer', True),
	(952, 'Marshall Crenshaw', True),
	(953, 'Robert Cray Band', True),
	(954, 'Junior Senior', True),
	(955, 'Magic Sam', True),
	(956, 'Art Tatum', True),
	(957, 'Bobby Fuller Four', True),
	(958, 'Usher', True),
	(959, 'House of Pain', True),
	(960, 'Four Tet', True),
	(961, 'Dismemberment Plan', True),
	(962, 'Fennesz', True),
	(963, 'Junior Murvin', True),
	(964, 'Lyle Lovett', True),
	(965, 'Toné Loc', False),
	(966, 'Jerry Butler', True),
	(967, 'Orange Juice', True),
	(968, 'En Vogue', True),
	(969, 'The United States of America', True),
	(970, 'Kings of Leon', True),
	(971, 'Roberta Flack', True),
	(972, 'Dr. Octagon', True),
	(973, 'George Clinton', True),
	(974, 'Bill Doggett', True),
	(975, 'Jill Scott', True),
	(976, 'Peter Brötzmann', True),
	(977, 'Les Paul & Mary Ford', True),
	(978, 'Ween', True),
	(979, 'Mary Margaret O''Hara', True),
	(980, 'Hot Hot Heat', True),
	(981, 'Chaka Khan', True),
	(982, 'Blind Faith', True),
	(983, 'Isolee', True),
	(984, 'The Pretty Things', True),
	(985, 'Tim Hardin', True),
	(986, 'Muse', True),
	(987, 'Coleman Hawkins', True),
	(988, 'Ultramagnetic MCs', True),
	(989, 'Steve Winwood', True),
	(990, 'Anita O''Day', True),
	(991, 'Clap Your Hands Say Yeah', True),
	(992, 'Veruca Salt', True),
	(993, 'Paul Weller', True),
	(994, 'Pantera', True),
	(995, 'Billy Idol', True),
	(996, 'Manitoba', True),
	(997, 'The Magic Numbers', True),
	(998, 'Planxty', True),
	(999, 'Social Distortion', True),
	(1000, 'Damien Rice', True),
	(1001, 'Chet Baker', True),
	(1002, 'The Go! Team', True),
	(1003, 'Red House Painters', True),
	(1004, 'Deutsch Amerikanische Freundschaft', True),
	(1005, 'M83', True),
	(1006, 'Adam and The Ants', True),
	(1007, 'The Sons of the Pioneers', True),
	(1008, 'Terence Trent D''Arby', True),
	(1009, 'The Wrens', True),
	(1010, 'The Easybeats', True),
	(1011, 'Warren G', True),
	(1012, 'Joan Baez', True),
	(1013, 'Backstreet Boys', True),
	(1014, 'Roger Miller', True),
	(1015, 'Kate Smith', True),
	(1016, 'Hank Mobley', True),
	(1017, 'Mark Lanegan', True),
	(1018, 'George McRae', True),
	(1019, 'The Tornados', True),
	(1020, 'Charlie Rich', True),
	(1021, 'Sunny Day Real Estate', True),
	(1022, 'Vashti Bunyan', True),
	(1023, 'Rythim Is Rythim', False),
	(1024, 'Clifton Chenier', True),
	(1025, 'The Chords', True),
	(1026, 'Sade', True),
	(1027, 'Os Mutantes', True),
	(1028, 'Tito Puente', True),
	(1029, 'The Hold Steady', True),
	(1030, 'Stevie Ray Vaughan', True),
	(1031, 'The Triffids', True),
	(1032, 'Kurtis Blow', True),
	(1033, 'Mudhoney', True),
	(1034, 'Lennie Tristano', True),
	(1035, 'Lionel Richie', True),
	(1036, 'Chris Isaak', True),
	(1037, 'Bob Wills and His Texas Playboys', True),
	(1038, 'Ice-T', True),
	(1039, 'The Auteurs', True),
	(1040, 'Pharrell Williams', True),
	(1041, 'Lipps Inc.', True),
	(1042, 'No Doubt', True),
	(1043, 'dEUS', True),
	(1044, 'Saint Etienne', True),
	(1045, 'Bachman-Turner Overdrive', True),
	(1046, 'John Fogerty', True),
	(1047, 'The Ventures', True),
	(1048, 'Patti Labelle', True),
	(1049, 'Barrett Strong', True),
	(1050, 'Spice Girls', True),
	(1051, 'Kim Carnes', True),
	(1052, 'The Sabres of Paradise', True),
	(1053, 'Cab Calloway', True),
	(1054, 'Bronski Beat', True),
	(1055, 'Jurassic 5', True),
	(1056, 'The Kingston Trio', True),
	(1057, 'Brenda Lee', True),
	(1058, 'Bikini Kill', True),
	(1059, 'Tom Tom Club', True),
	(1060, 'Temple of the Dog', True),
	(1061, 'Tony Bennett', True),
	(1062, 'Ms. Dynamite', True),
	(1063, 'Ali Farka Toure', True),
	(1064, 'Slick Rick', True),
	(1065, 'The Dixie Cups', True),
	(1066, 'T-Bone Walker', True),
	(1067, 'Annie', True),
	(1068, 'Ketty Lester', True),
	(1069, 'Sonny and Cher', True),
	(1070, 'Johnny Horton', True),
	(1071, 'Queensryche', True),
	(1072, 'The Style Council', True),
	(1073, 'Lefty Frizzell', True),
	(1074, 'Petula Clark', True),
	(1075, 'Peggy Lee', True),
	(1076, 'Jimmie Davis', True),
	(1077, 'Flipper', True),
	(1078, 'Pete Townshend', True),
	(1079, 'The Champs', True),
	(1080, 'Death in Vegas', True),
	(1081, 'The Sundays', True),
	(1082, 'Herbert', True),
	(1083, 'Stephen Stills', True),
	(1084, 'Mazzy Star', True),
	(1085, 'Blind Lemon Jefferson', True)
	ON CONFLICT
	DO NOTHING;
/*!40000 ALTER TABLE "artists" ENABLE KEYS */;

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
