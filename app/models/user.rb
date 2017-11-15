# frozen_string_literal: true

class User < ApplicationRecord
  # Include default devise modules. Others available are:
  # :confirmable, :lockable, :timeoutable and :omniauthable
  devise :database_authenticatable, :registerable,
         :recoverable, :rememberable, :trackable, :validatable
  has_many :job_types
  has_many :workers
  has_many :event_receivers
  has_many :jobs, through: :job_types
  has_many :api_keys

  after_create :make_info_channel

  def info_channel
    WebsocketRails["user.#{id}"]
  end

  private

  def make_info_channel
    info_channel.make_private
  end
end
