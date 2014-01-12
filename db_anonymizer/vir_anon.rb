# encoding: utf-8
#/usr/bin/ruby -w

require 'rubygems'
require 'yaml'
require 'sequel'
require 'logger'

require_relative 'user.rb'

LOGGER = Logger.new('logs/result.log')

config_file = File.join File.dirname(__FILE__), "config.yml"
config = YAML.load_file config_file

$DB = Sequel.postgres config["database"]

def update_user(record)
  user = User.new record
  $DB[:users].where('usr_id = ?', user.id).update(user.get_anonimized_attrs)
end

begin
  time_begin = Time.now

  $DB.transaction do # BEGIN
    $DB[:users].each { |record|
      update_user(record)
    }

    LOGGER.info 'truncate some tables...'
    $DB.run('truncate table neptun_list cascade')
    $DB.run('truncate table lostpw_tokens')
    $DB.run('truncate table spot_images')
  end # COMMIT

  LOGGER.info "Finished. Elapsed time=" + (Time.now - time_begin).to_s

rescue Exception => e
  LOGGER.ERROR e.message
  puts e.message
  exit
end
