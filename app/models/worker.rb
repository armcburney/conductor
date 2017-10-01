# frozen_string_literal: true

class Worker < ApplicationRecord
  extend FriendlyId

  friendly_id :address, use: :slugged

  belongs_to :user
  has_many :jobs
end
