require_relative 'spec_helper.rb'

describe User do

  TEST_RECORD = {
    :usr_id => '5',
    :usr_email => 'wow-such-private@doge.gov',
    :usr_neptun => 'WoWLoL',
    :usr_firstname => 'Anti',
    :usr_lastname => 'Atom',
    :usr_nickname => 'joker',
    :usr_date_of_birth => '18790314',
    :usr_gender => 'UNKNOWN',
    :usr_mother_name => 'Re Barbara',
    :usr_photo_path => 'notempty',
    :usr_webpage => 'http://stackoverflow.com',
    :usr_cell_phone => '+36201234567',
    :usr_home_address => 'Hawaii',
    :usr_dormitory => 'Schönherz',
    :usr_room => '42',
    :usr_confirm => 'xxxxxx',
    :usr_lastlogin => '2012-12-21',
    :usr_password => 'orig_hash',
    :usr_salt => 'orig_salt'
  }

  before :each do
    @user = User.new (TEST_RECORD)
  end

  describe "#init" do
    it "should save the id when create" do
      expect(@user.id).to be(TEST_RECORD[:usr_id])
    end
  end

  describe "#valid" do
    before :each do
      u = User.new({
        :usr_id => '6',
        :usr_firstname => ''
        })

      @anon_attrs = u.get_anonimized_attrs
    end

    it "should leave empty field untouched" do
      expect(@anon_attrs[:usr_firstname]).to be_nil
    end

    it "should not add nonexistent field" do
      expect(@anon_attrs[:usr_lastname]).to be_nil
    end
  end

  describe "#get_anonimized_attrs" do
    before :each do
      @anon_attrs = @user.get_anonimized_attrs
    end

    it "should replace the email indexed by id" do
      expect(@anon_attrs[:usr_email]).to start_with("pek.juzer#{@user.id}@")
    end

    it "should replace the neptun indexed by id" do
      expect(@anon_attrs[:usr_neptun]).to eq('A'+("%05d" % [@user.id]))
    end

    it "should replace the firstname indexed by id" do
      expect(@anon_attrs[:usr_firstname]).to eq("Júzer #{@user.id}")
    end

    it "should replace the lastname" do
      expect(@anon_attrs[:usr_lastname]).to eq("Pék")
    end

    it "should replace the nickname indexed by id" do
      expect(@anon_attrs[:usr_nickname]).to eq("pék #{@user.id}")
    end

    it "should remove the birthday" do
      expect(@anon_attrs[:usr_date_of_birth]).to be_nil
    end

    it "should set gender to notspecified" do
      expect(@anon_attrs[:usr_gender]).to eq('NOTSPECIFIED')
    end

    it "should remove the name of mother" do
      expect(@anon_attrs[:usr_mother_name]).to be_nil
    end

    it "should remove the photo" do
      expect(@anon_attrs[:usr_photo_path]).to be_nil
    end

    it "should remove the webpage" do
      expect(@anon_attrs[:usr_webpage]).to be_nil
    end

    it "should remove the cell phone" do
      expect(@anon_attrs[:usr_cell_phone]).to be_nil
    end

    it "should remove the home address" do
      expect(@anon_attrs[:usr_home_address]).to be_nil
    end

    it "should remove the dormitory" do
      expect(@anon_attrs[:usr_dormitory]).to be_nil
    end

    it "should remove the room" do
      expect(@anon_attrs[:usr_room]).to be_nil
    end

    it "should remove the confirmation code" do
      expect(@anon_attrs[:usr_confirm]).to be_nil
    end

    it "should remove the lastlogin date" do
      expect(@anon_attrs[:usr_lastlogin]).to be_nil
    end

    it "should replace user password" do
      expect(@anon_attrs[:usr_password]).not_to be(nil)
      expect(@anon_attrs[:usr_password]).not_to be(TEST_RECORD[:usr_password])
    end

    it "should replace user salt" do
      expect(@anon_attrs[:usr_salt]).not_to be(nil)
      expect(@anon_attrs[:usr_salt]).not_to be(TEST_RECORD[:usr_salt])
    end

  end
end
