# frozen_string_literal: true

class JobType < ApplicationRecord
  before_save :nullify_blanks

  belongs_to :user
  has_many :jobs

  private

  def nullify_blanks
    environment_variables = "{}" if environment_variables&.empty?
    working_directory = nil if working_directory&.empty?
  end
end
