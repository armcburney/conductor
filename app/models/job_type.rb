# frozen_string_literal: true

class JobType < ApplicationRecord
  belongs_to :user
  has_many :jobs
end
