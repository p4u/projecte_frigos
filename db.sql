CREATE TABLE IF NOT EXISTS `Lectura` (
    `ID` int(11) NOT NULL AUTO_INCREMENT,
      `data` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
        `trasto_id` char(64) CHARACTER SET latin1 COLLATE latin1_spanish_ci NOT NULL,
          `intensitat` float DEFAULT NULL,
            `tensio` float DEFAULT NULL,
              `temperatura1` float DEFAULT NULL,
                `temperatura2` float DEFAULT NULL,
                  PRIMARY KEY (`ID`)
                  ) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=0 ;

                  -- --------------------------------------------------------

CREATE TABLE IF NOT EXISTS `Recolector` (
    `ID` char(32) NOT NULL,
      `data_vist` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        PRIMARY KEY (`ID`)
        ) ENGINE=InnoDB DEFAULT CHARSET=latin1;

        -- --------------------------------------------------------

CREATE TABLE IF NOT EXISTS `Trasto` (
    `ID` char(64) CHARACTER SET latin1 COLLATE latin1_spanish_ci NOT NULL,
      `nom` text CHARACTER SET latin1 COLLATE latin1_spanish_ci,
        `recolector_id` char(32) NOT NULL,
          `tipus` text CHARACTER SET latin1 COLLATE latin1_spanish_ci NOT NULL,
            `data_creacio` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
              PRIMARY KEY (`ID`)
              ) ENGINE=InnoDB DEFAULT CHARSET=latin1;

