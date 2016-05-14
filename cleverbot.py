import discord
from cleverbot import Cleverbot
import math
import re
import time

client = discord.Client()
cb = Cleverbot();
cookietimer = 0;

import pymysql.cursors

handle = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='',
                             db='cleverbot',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

def xquadratic(a, b, c):
    soln = str();
    if( a*c*-4.0+b*b < 0 ):
        return "I do not support complex numbers, just yet!";
    
    x1 = (b*(-1.0/2.0)-math.sqrt(a*c*-4.0+b*b)*(1.0/2.0))/a;
    x2 = (b*(-1.0/2.0)+math.sqrt(a*c*-4.0+b*b)*(1.0/2.0))/a;
    soln = "x1 = %d, x2 = %d" % ( x1, x2 );
    return soln;


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!givecookie'):
        global cookietimer;
        if( cookietimer < int( time.time() ) ):
            user = message.content[12:];
            if( not user ):
                return await client.send_message( message.channel, "!cookie [@user]" );

            if( user == message.author.mention ):
                return await client.send_message( message.channel, "%s is trying too hard for cookies!" % ( user ) );
            cur = handle.cursor();
            sql = "SELECT * FROM users WHERE user = %s;";
            cur.execute( sql, (user) );
            handle.commit();
            data = cur.fetchone();
            if( not data ):
                sql = "INSERT INTO users SET user = '%s', cookies = '%d';" % ( user, 1 );
                cur.execute( sql );
                print( sql );
            else:
                sql = "UPDATE users SET cookies = %d WHERE user = '%s';" % ( data['cookies'] + 1, user );
                cur.execute( sql );
                print( sql );
            handle.commit();
            await client.send_message( message.channel, "%s has given %s a cookie." % ( message.author.mention, user ) );
            cookietimer = int( time.time() ) + 180;
            return;
        await client.send_message( message.channel, "Another cookie can be given in: %d seconds." % ( cookietimer - int( time.time() ) ) );
        
        return;

    if message.content.startswith( '!cookies' ):
        user = message.content[9:];
        cur = handle.cursor();
        if not user or user == message.author.name:
            user = message.author.mention;
            cur = handle.cursor();
            sql = "SELECT * FROM users WHERE user = '%s';" % user;
            cur.execute( sql );

            data = cur.fetchone();
            if( data ):
                await client.send_message( message.channel, "%s has %d cookie%s." % ( user, data['cookies'], '' if data['cookies']==1 else 's') );
                return
            await client.send_message( message.channel, "%s has no cookies." % ( user ) );
            return;
    

        sql = "SELECT * FROM users WHERE user = %s;";
        cur.execute( sql, (user) );
        handle.commit();

        data = cur.fetchone();
        if( data ):
            await client.send_message( message.channel, "%s has %d cookie(s)." % ( data['user'], data['cookies'] ) );
        else:
            await client.send_message( message.channel, "No user found in the database." );
        return;
    
    if message.content.startswith('!todo add'):
        task = message.content[10:];
        cur = handle.cursor();
        sql = "INSERT INTO `cleverbot` (`task`) VALUES (%s)"
        cur.execute(sql, ( task ) )
        handle.commit();


        await client.send_message(message.channel, "I have added the task: %s." % task );
        return

    if message.content.startswith( '!todo show'):
        cur = handle.cursor();
        cur.execute( "SELECT * FROM cleverbot" );
        handle.commit();
        show = message.author;
        if( message.content[11:] == "all" ):
            show = message.channel;
        count = 0;
        data = cur.fetchall();
        if( len( data ) > 0 ):
            for row in data:
                count += 1;
                if( count == 6 ):
                    await client.send_message( show, "There's more, but I don't want to spam the channel!" );
                    break;
                await client.send_message( show, ( "%d. Task: %s\ncompletes: %s." % ( row['id'], row['task'], row['completes'] ) ) );
        else:
            await client.send_message( show, "There's nothing to show." );
        return

    if message.content.startswith( '!todo delete'):
        cur = handle.cursor();
        id = message.content[13:];
        try: id = int( id );
        except: await client.send_message( message.author, "!todo delete [id]" ); return;
        cur.execute( "DELETE FROM cleverbot WHERE id = %d;" % id );
        await client.send_message( message.channel, "I have deleted the task ID: %d" % id );
        print( id );
        return;

    if message.content.startswith( '!todo complete' ):
        cur = handle.cursor();
        id = message.content[15:];
        print( message.content );
        try: id = int(id);
        except: await client.send_message( message.author, "!todo complete [id]" ); return;
        sql = "SELECT * FROM cleverbot WHERE id = %d;" % id;
        cur.execute( sql );

        data = cur.fetchone();
        if( not data ):
            return await client.send_message( message.author, "You specified an invalid task ID." );
        names = data['completes'];
        id = data['id'];
                   
        if( names == None ):
            names = message.author.mention;
        else:
            names = "%s, %s" % ( names, message.author.mention );
        print( names );
        sql = "UPDATE cleverbot SET completes = '%s' WHERE id = %d" % (names, id) ;
        print( sql );
        cur.execute( sql )
        handle.commit();
        await client.send_message( message.channel, "%s has completed task ID %d." % ( message.author.mention, id ) );
        
        
    if message.content.startswith('!quad'):
        values = message.content[6:].split();
        for i in range( 0, len( values ) ):
            try: values[i] = int( values[i] );
            except: return await client.send_message(message.channel, "Oops, you entered an invalid data time!" );

        msg = str();
        soln = xquadratic(values[0], values[1], values[2]);
        msg = "The solutions to the equation: %dx^2 " % values[0];
        if( values[1] > 0 ):
            msg += "+ %dx " % values[1];
        elif( values[1] < 0 ):
            msg += "%dx " % values[1];
        else:
            pass;
        if( values[2] > 0 ):
            msg += "+ %d " % values[2];
        elif( values[2] < 0 ):
            msg += " %d " % values[2];
        else:
            pass;
    
        msg +=  "are:\n%s" % soln;
        
        await client.send_message(message.channel, msg );
        return

    if message.content.startswith('!calc'):
        msg = message.content[6:];
        if( re.match( "[-+*]?[0-9]*\.?[0-9]", msg ) ):
            try:
                ans = eval( message.content[6:] );
            except:
                await client.send_message( message.channel, "The equation you've given seems wrong, hm." );

            await client.send_message( message.channel, ( "The answer is %0.2f" % ans ) );
            return
        await client.send_message( message.channel, ( "The question you've given seems wrong, hm." ) );
        return;
        

@client.event
async def on_ready():
    print('Connected with username %s, userID: %s' % ( client.user.name, client.user.id ) );


client.run('MTgwNjQ3Nzk0MjMzNzA0NDQ4.ChdQ3g.KohgkcxwMQZ9rkpbZXdEbeys3Kg')
handle.close();
