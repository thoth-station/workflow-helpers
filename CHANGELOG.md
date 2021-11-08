# Changelog for Thoth's Template GitHub Project

## Release 0.9.4 (2021-11-08T20:25:32)
* :arrow_up: Automatic update of dependencies by Kebechet for the ubi8 environment

## Release 0.9.3 (2021-10-29T19:40:33)
* :arrow_up: Automatic update of dependencies by Kebechet for the ubi8 environment
* add cwd context from common instead of keb
* :arrow_up: Automatic update of dependencies by Kebechet for the ubi8 environment

## Release 0.9.2 (2021-10-11T13:22:37)
### Features
* Remove missed parameter
* :arrow_up: Automatic update of dependencies by Kebechet for the ubi8 environment

## Release 0.9.1 (2021-09-27T20:58:19)
### Features
* :arrow_up: Automatic update of dependencies by Kebechet for the ubi8 environment
* manage installation runtime environments

## Release 0.9.0 (2021-09-14T20:59:55)
### Features
* Update of the dependencies
* create new wfh task which initializes a repo with .thoth.yaml and example advise
* add list of available runtimes to purge issue (#326)
* set empty default to label
* Add trigger type to the metrics to know how many messages are creted per trigger

## Release 0.8.9 (2021-08-24T10:52:41)
### Features
* Fix kebechet administrator scheduling

## Release 0.8.8 (2021-08-19T10:09:34)
### Features
* Fix env variable in kebechet administrator
* storages function uses wrong name
### Improvements
* Refactor methods for metrics (#304)

## [0.1.0] - 2019-Sep-11 - goern

### Added

all the things that you see...

## Release 0.1.1 (2020-07-27T16:33:47)
* Add method to produce inputs for Kafka CLI (#25)
* fixes issue 21 (#26)
* More robust app.sh (#20)
* :pushpin: Automatic update of dependency thoth-common from 0.13.13 to 0.14.2 (#24)
* :pushpin: Automatic update of dependency thoth-common from 0.13.13 to 0.14.2 (#23)
* :pushpin: Automatic update of dependency thamos from 0.10.5 to 0.10.6 (#22)
* :pushpin: Automatic dependency re-locking
* Update OWNERS
* :pushpin: Automatic update of dependency thoth-python from 0.9.2 to 0.10.0
* :pushpin: Automatic update of dependency thoth-common from 0.13.11 to 0.13.12
* Update OWNERS
* Create OWNERS
* prefix env variables with thoth
* address comments
* create workflow helper for downloading pypackage
* add env variables and modify zuul yaml
* Add error type
* Improve readme
* same change as above
* small bugs
* Remove import

## Release 0.1.2 (2020-08-05T13:50:54)
* :pushpin: Automatic update of dependency thoth-common from 0.14.2 to 0.16.0 (#32)
* parse git service and remove f.close(context managers) (#31)

## Release 0.1.3 (2020-08-11T13:35:06)
* :pushpin: Automatic update of dependency thoth-python from 0.10.0 to 0.10.1 (#40)
* :pushpin: Automatic update of dependency thamos from 0.10.6 to 0.11.0 (#39)
* :pushpin: Automatic update of dependency thamos from 0.10.6 to 0.11.0 (#38)
* Use custom name for file (#36)

## Release 0.1.4 (2020-09-02T14:26:53)
### Features
* Update files (#50)
* Add pre-commit and correct errors (#49)
* Consider multiple indexes (#46)
* :truck: include aicoe-ci configuration file (#43)
### Improvements
* Add message content for service name and version sending Kafka Messages (#52)
* Add parse solved method (#44)
### Automatic Updates
* :pushpin: Automatic update of dependency thamos from 0.11.1 to 0.12.0 (#55)
* :pushpin: Automatic update of dependency thamos from 0.11.1 to 0.12.0 (#54)
* :pushpin: Automatic update of dependency thamos from 0.11.0 to 0.11.1 (#47)

## Release 0.1.5 (2020-09-09T13:44:07)
### Features
* Fix metadata missing in adviser workflow (#63)
* :turtle: update base image to be used for build. (#60)
### Automatic Updates
* :pushpin: Automatic update of dependency thoth-common from 0.17.2 to 0.17.3 (#62)
* :pushpin: Automatic update of dependency thamos from 0.12.0 to 0.12.2 (#59)

## Release 0.1.6 (2020-09-11T13:23:41)
### Features
* Change name because overwrite Argo default (#67)
### Automatic Updates
* :pushpin: Automatic update of dependency thoth-storages from 0.25.6 to 0.25.7 (#70)
* :pushpin: Automatic update of dependency thoth-storages from 0.25.6 to 0.25.7 (#69)
* :pushpin: Automatic update of dependency thoth-common from 0.17.3 to 0.18.1 (#68)
* :pushpin: Automatic update of dependency thoth-storages from 0.25.5 to 0.25.6 (#66)

## Release 0.1.7 (2020-09-11T15:35:48)
### Features
* Add info version (#73)
### Automatic Updates
* :pushpin: Automatic update of dependency thoth-common from 0.18.1 to 0.18.2 (#75)

## Release 0.1.8 (2020-09-15T08:43:01)
### Features
* Use correct value (#83)
* Make pre-commit happy (#79)
* Show all thoth libraries versions in logs (#78)
### Automatic Updates
* :pushpin: Automatic update of dependency thoth-storages from 0.25.7 to 0.25.8 (#81)
* :pushpin: Automatic update of dependency thoth-common from 0.18.2 to 0.18.3 (#80)

## Release 0.1.9 (2020-09-15T11:29:02)
### Features
* Store file always to avoid workflow failing (#82)
### Automatic Updates
* :pushpin: Automatic update of dependency thamos from 0.12.2 to 1.0.0 (#88)

## Release 0.1.10 (2020-09-16T07:00:18)
### Improvements
* Add more logs (#95)
### Automatic Updates
* :pushpin: Automatic update of dependency thoth-storages from 0.25.8 to 0.25.9 (#94)
* :pushpin: Automatic update of dependency thoth-common from 0.18.3 to 0.19.0 (#91)

## Release 0.1.11 (2020-09-17T08:13:51)
### Features
* Show messages sent (#98)
### Automatic Updates
* :pushpin: Automatic update of dependency thoth-storages from 0.25.9 to 0.25.10 (#100)

## Release 0.1.12 (2020-09-17T09:30:10)
### Features
* Add missing ' (#103)

## Release 0.1.13 (2020-09-25T06:10:52)
### Features
* parse solver document (#107)
* :nut_and_bolt: store default empty string for other source types (#110)
### Automatic Updates
* :pushpin: Automatic update of dependency thoth-storages from 0.25.10 to 0.25.11 (#119)
* :pushpin: Automatic update of dependency thoth-storages from 0.25.10 to 0.25.11 (#118)
* :pushpin: Automatic update of dependency thoth-python from 0.10.1 to 0.10.2 (#117)
* :pushpin: Automatic update of dependency thoth-python from 0.10.1 to 0.10.2 (#116)
* :pushpin: Automatic update of dependency thoth-python from 0.10.1 to 0.10.2 (#115)
* :pushpin: Automatic update of dependency thoth-common from 0.19.0 to 0.20.0 (#114)
* :pushpin: Automatic update of dependency thoth-common from 0.19.0 to 0.20.0 (#113)
* :pushpin: Automatic update of dependency thoth-common from 0.19.0 to 0.20.0 (#112)

## Release 0.1.14 (2020-10-02T08:14:58)
### Features
* Correct import and add defaults (#128)
* Feature/is analyzable message (#122)
### Automatic Updates
* :pushpin: Automatic update of dependency thoth-messaging from 0.7.8 to 0.7.10 (#126)
* :pushpin: Automatic update of dependency thoth-storages from 0.25.13 to 0.25.14 (#125)
* :pushpin: Automatic update of dependency thoth-storages from 0.25.13 to 0.25.14 (#124)

## Release 0.1.15 (2020-10-02T10:24:06)
### Features
* Assign datatype in message (#132)
### Bug Fixes
* Do not fail on known errors (#131)

## Release 0.1.16 (2020-10-07T16:49:57)
### Features
* Qebhwt workflow now saves the adviser message (#136)
### Automatic Updates
* :pushpin: Automatic update of dependency thoth-storages from 0.25.14 to 0.25.15 (#140)
* :pushpin: Automatic update of dependency thoth-messaging from 0.7.10 to 0.7.11 (#139)
* :pushpin: Automatic update of dependency thoth-storages from 0.25.14 to 0.25.15 (#138)

## Release 0.1.17 (2020-10-12T06:23:04)
### Features
* Fixed source tpye not parseable" (#143)
### Automatic Updates
* :pushpin: Automatic update of dependency thoth-common from 0.20.0 to 0.20.1 (#145)

## Release 0.1.18 (2020-10-15T17:15:19)
### Features
* Add method to send unresolved packages message from adviser report inspection (#150)
### Automatic Updates
* :pushpin: Automatic update of dependency thoth-messaging from 0.7.11 to 0.7.13 (#149)

## Release 0.1.19 (2020-10-20T08:54:45)
### Features
* Do not return before saving default (#156)
* Method should not fail and output default always present (#155)
* lock down thoth-messaging (#153)

## Release 0.2.0 (2020-11-30T20:30:08)
### Features
* Kebechet admin (#154)
* :arrow_up: Automatic update of dependencies by kebechet. (#170)
### Automatic Updates
* :pushpin: Automatic update of dependency thoth-storages from 0.25.15 to 0.25.16 (#165)
* :pushpin: Automatic update of dependency thoth-storages from 0.25.15 to 0.25.16 (#164)
* :pushpin: Automatic update of dependency thoth-common from 0.20.2 to 0.20.4 (#163)
* :pushpin: Automatic update of dependency thoth-common from 0.20.2 to 0.20.4 (#162)
* :pushpin: Automatic update of dependency thamos from 1.0.1 to 1.1.1 (#161)
* :pushpin: Automatic update of dependency thoth-common from 0.20.1 to 0.20.2 (#160)
* :pushpin: Automatic update of dependency thoth-common from 0.20.1 to 0.20.2 (#159)

## Release 0.3.0 (2020-11-30T21:05:16)
### Features
* Add graph schema update task (#168)

## Release 0.3.1 (2020-12-01T07:33:29)
### Features
* :arrow_up: Automatic update of dependencies by kebechet. (#181)
* Update .thoth.yaml (#172)
* :arrow_up: Automatic update of dependencies by kebechet. (#179)
* Add pre-commit (#175)

## Release 0.3.2 (2021-01-11T08:50:36)
### Features
* Send also runtime environment in adviser trigger message (#187)
* :arrow_up: Automatic update of dependencies by kebechet. (#185)
* :arrow_up: Automatic update of dependencies by kebechet. (#184)
* get inspection info from env (#167)

## Release 0.3.3 (2021-01-12T12:30:12)
### Bug Fixes
* Always store file to avoid error in Argo (#192)

## Release 0.4.0 (2021-01-27T07:36:29)
### Features
* Introduce metrics for revision (#197)
* :arrow_up: Automatic update of dependencies by kebechet. (#196)
* :arrow_up: Automatic update of dependencies by kebechet. (#188)
* update to latest messaging (#195)
### Improvements
* change message contents of inspection complete (#198)

## Release 0.4.1 (2021-02-01T15:22:59)
### Features
* Add kebechet templates (#205)
* :arrow_up: Automatic update of dependencies by kebechet. (#206)
* :arrow_up: Automatic update of dependencies by kebechet. (#202)

## Release 0.5.0 (2021-02-02T06:56:44)
### Improvements
* Add parse provenance check method (#203)

## Release 0.6.0 (2021-02-16T20:51:35)
### Features
* add new param for v2 of run-url message (#215)
* :arrow_up: Automatic update of dependencies by Kebechet (#220)
* keep message file contents (#219)
* permission must be single char (#217)
* :arrow_up: Automatic update of dependencies by Kebechet (#218)
* Update OWNERS
* :arrow_up: Automatic update of dependencies by Kebechet (#216)
* :arrow_up: Automatic update of dependencies by Kebechet (#214)
### Improvements
* Introduce metrics for messages sent and enforce consistency (#212)

## Release 0.6.1 (2021-03-19T13:18:07)
### Features
* configure ci/cd prow on the app
* :arrow_up: Automatic update of dependencies by Kebechet (#225)

## Release 0.6.2 (2021-03-28T05:38:27)
### Features
* constrain thoth-messaging (#228)

## Release 0.7.0 (2021-04-16T06:59:09)
### Features
* Adjust adviser rerun logic (#240)
* Messaging pydantic (#236)
* :arrow_up: Automatic update of dependencies by Kebechet (#237)
* :arrow_up: Automatic update of dependencies by Kebechet (#233)
* Adjust AdviserTrigger message (#234)
### Improvements
* Use thamos and not messaging for qeb-hwt workflow (#239)
* remove extra message contents removed in v2 (#229)

## Release 0.7.1 (2021-04-16T16:59:52)
### Features
* Adjust input to thamos method (#245)

## Release 0.8.0 (2021-05-06T07:46:05)
### Features
* :arrow_up: Automatic update of dependencies by Kebechet (#254)
* adjust metric name (#252)
* :arrow_up: Automatic update of dependencies by Kebechet (#248)
### Bug Fixes
* use python 3.8 fixes pydantic issues (#250)
* __all__ was imported as all messages (#249)

## Release 0.8.1 (2021-05-19T13:12:46)
### Bug Fixes
* package_version param was wrong (#256)

## Release 0.8.2 (2021-06-14T20:17:39)
### Features
* :arrow_up: Automatic update of dependencies by Kebechet (#269)
* :arrow_up: Automatic update of dependencies by Kebechet
* return to_ret
* :arrow_up: Automatic update of dependencies by Kebechet
* :arrow_up: Automatic update of dependencies by Kebechet
* enable sending missing package messages
### Bug Fixes
* mypy error fix for workflow-helpers (#270)

## Release 0.8.3 (2021-06-15T12:29:27)
### Features
* :arrow_up: Automatic update of dependencies by Kebechet
### Bug Fixes
* Relock to fix missing typing_extensions

## Release 0.8.4 (2021-06-24T05:18:09)
### Features
* :arrow_up: Automatic update of dependencies by Kebechet
* :arrow_up: Automatic update of dependencies by Kebechet

## Release 0.8.5 (2021-06-30T03:05:26)
### Features
* :arrow_up: Automatic update of dependencies by Kebechet

## Release 0.8.6 (2021-07-02T06:52:13)
### Features
* :arrow_up: Automatic update of dependencies by Kebechet (#297)
* :arrow_up: Automatic update of dependencies by Kebechet (#295)
* Use common enums
* Deprecate qeb-hwt
* new workflow helpers task to update keb installation in DB
### Bug Fixes
* :cloud: mypy fixes for the workflow-helpers
### Improvements
* Clean methods and README (#293)

## Release 0.8.7 (2021-07-30T10:31:00)
### Features
* :arrow_up: Automatic update of dependencies by Kebechet (#307)
* :arrow_up: Automatic update of dependencies by Kebechet
* Fix sending metric twice
* add new script for opening issues on data purge
* :arrow_up: Automatic update of dependencies by Kebechet
* add more args for issue/pr context and adviser update runs
