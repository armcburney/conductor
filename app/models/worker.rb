# frozen_string_literal: true

class Worker < ApplicationRecord
  belongs_to :user
  has_many :jobs
end
