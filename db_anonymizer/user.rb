class User
  attr_accessor :id
  EMPTY = ''
  # salted hash of 'alma123'
  PASSWORD_HASH = 'gINhBG2Jdq/fSU3LlMKbqUOH++Y='
  PASSWORD_SALT = 'ZFf391apIxE='

  UNTOUCHED_FIELDS = [
    :usr_id, :usr_svie_state, :usr_svie_member_type,
    :usr_svie_primary_membership, :usr_delegated,
    :usr_show_recommended_photo, :usr_screen_name,
    :usr_status, :usr_student_status, :usr_est_grad
  ]

  CLEAR_FIELDS = [
    :usr_date_of_birth, :usr_mother_name, :usr_photo_path,
    :usr_webpage, :usr_cell_phone, :usr_home_address,
    :usr_dormitory, :usr_room, :usr_confirm, :usr_lastlogin
  ]

  def initialize(record)
    @id = record[:usr_id]
    @record = record
  end

  def get_anonimized_attrs
    attrs = {}

    @record.each { |key, value|
      unless UNTOUCHED_FIELDS.include? key
        if CLEAR_FIELDS.include? key
          attrs[key] = nil
        elsif valid?(value)
          attrs[key] = send "anon_#{key}"
        end
      end
    }

    attrs
  end

  private

    def valid?(value)
      value != nil and !value.to_s.empty?
    end

    # attribute anonimizer methods

    def anon_usr_email
      "pek.juzer#{@id}@devnull.stewie.sch.bme.hu"
    end

    def anon_usr_neptun
      'A'+("%05d" % [@id])
    end

    def anon_usr_firstname
      "Júzer #{@id}"
    end

    def anon_usr_lastname
      'Pék'
    end

    def anon_usr_nickname
      "pék #{@id}"
    end

    def anon_usr_gender
      'NOTSPECIFIED'
    end

    def anon_usr_password
      PASSWORD_HASH
    end

    def anon_usr_salt
      PASSWORD_SALT
    end

end
