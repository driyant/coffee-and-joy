/*==============================================================*/
/* DBMS name:      MySQL 5.0                                    */
/* Created on:     13/09/2021 07:44:00                          */
/*==============================================================*/


/*==============================================================*/
/* Table: CATEGORY                                              */
/*==============================================================*/
create table CATEGORY
(
   ID_CATEGORY          int not null  comment '',
   CATEGORY_NAME        varchar(50)  comment '',
   primary key (ID_CATEGORY)
);

/*==============================================================*/
/* Table: EVENT                                                 */
/*==============================================================*/
create table EVENT
(
   ID_EVENT             int not null  comment '',
   EVENT_NAME           varchar(100)  comment '',
   EVENT_DESCRIPTION    varchar(255)  comment '',
   EVENT_PLACE          varchar(100)  comment '',
   EVENT_DATE           datetime  comment '',
   primary key (ID_EVENT)
);

/*==============================================================*/
/* Table: MENU                                                  */
/*==============================================================*/
create table MENU
(
   ID_MENU              int not null  comment '',
   ID_CATEGORY          int  comment '',
   MENU_NAME            varchar(50)  comment '',
   MENU_DESCRIPTION     varchar(50)  comment '',
   MENU_PHOTO           longtext  comment '',
   primary key (ID_MENU)
);

/*==============================================================*/
/* Table: SUBSCRIBER                                            */
/*==============================================================*/
create table SUBSCRIBER
(
   ID_SUBSCRIBER        int not null  comment '',
   FIRSTNAME            varchar(50)  comment '',
   LASTNAME             varchar(50)  comment '',
   EMAIL                varchar(50)  comment '',
   primary key (ID_SUBSCRIBER)
);

alter table MENU add constraint FK_MENU_CONSIST_O_CATEGORY foreign key (ID_CATEGORY)
      references CATEGORY (ID_CATEGORY) on delete restrict on update restrict;

